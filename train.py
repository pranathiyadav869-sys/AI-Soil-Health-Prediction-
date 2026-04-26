"""
=============================================================
 Loss Functions + Training Loop
=============================================================
"""

import time
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.optim import AdamW
from torch.optim.lr_scheduler import CosineAnnealingLR
import numpy as np
from sklearn.metrics import r2_score, classification_report, confusion_matrix


# ─────────────────────────────────────────────────────────
# 1. Focal Loss  (handles class imbalance in classification)
# ─────────────────────────────────────────────────────────
class FocalLoss(nn.Module):
    """
    WHY Focal Loss instead of plain CrossEntropy?
    - Standard CE treats all samples equally
    - Focal Loss down-weights easy examples (γ > 0) and focuses
      training on hard, misclassified samples
    - Combined with class weights (α) it doubly handles imbalance:
        α corrects for frequency imbalance
        γ corrects for difficulty imbalance
    - Formula: FL(p_t) = -α_t · (1 - p_t)^γ · log(p_t)
    - γ=2 is the standard choice; reduce to γ=1 if training is unstable
    """
    def __init__(self, alpha: torch.Tensor = None, gamma: float = 2.0):
        super().__init__()
        self.alpha = alpha      # (n_classes,) class weights tensor
        self.gamma = gamma

    def forward(self, logits: torch.Tensor, targets: torch.Tensor):
        ce_loss = F.cross_entropy(logits, targets, weight=self.alpha, reduction="none")
        pt = torch.exp(-ce_loss)                      # probability of true class
        focal_loss = (1 - pt) ** self.gamma * ce_loss
        return focal_loss.mean()


# ─────────────────────────────────────────────────────────
# 2. Combined Loss (regression + classification)
# ─────────────────────────────────────────────────────────
class CombinedLoss(nn.Module):
    """
    WHY multi-task loss?
    - Jointly optimising regression + classification forces the shared
      trunk to learn features useful for BOTH tasks
    - Regression regularises classification → smoother decision boundaries
    - λ controls the balance; start with 1.0 and tune if needed

    Total = MSE(shi_pred, shi_true) + λ · FocalLoss(logits, class_true)
    """
    def __init__(self, class_weights: torch.Tensor, gamma: float = 2.0,
                 lambda_cls: float = 1.0):
        super().__init__()
        self.mse        = nn.MSELoss()
        self.focal      = FocalLoss(alpha=class_weights, gamma=gamma)
        self.lambda_cls = lambda_cls

    def forward(self, shi_pred, logits, shi_true, class_true):
        reg_loss = self.mse(shi_pred, shi_true)
        cls_loss = self.focal(logits, class_true)
        total    = reg_loss + self.lambda_cls * cls_loss
        return total, reg_loss.item(), cls_loss.item()


# ─────────────────────────────────────────────────────────
# 3. Training utilities
# ─────────────────────────────────────────────────────────
def train_one_epoch(model, loader, optimizer, loss_fn, device):
    model.train()
    total_loss = reg_loss_sum = cls_loss_sum = 0.0
    all_shi_true, all_shi_pred = [], []
    all_cls_true, all_cls_pred = [], []

    for batch in loader:
        tabular    = batch["tabular"].to(device)
        ts         = batch["ts"].to(device)
        img        = batch["img"].to(device)
        shi_true   = batch["shi"].to(device)
        class_true = batch["soil_class"].to(device)

        optimizer.zero_grad()
        shi_pred, logits = model(tabular, ts, img)
        loss, r, c = loss_fn(shi_pred, logits, shi_true, class_true)
        loss.backward()

        # Gradient clipping → prevents exploding gradients in LSTM
        nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()

        total_loss    += loss.item()
        reg_loss_sum  += r
        cls_loss_sum  += c

        all_shi_true.extend(shi_true.cpu().numpy())
        all_shi_pred.extend(shi_pred.detach().cpu().numpy())
        all_cls_true.extend(class_true.cpu().numpy())
        all_cls_pred.extend(logits.argmax(dim=-1).detach().cpu().numpy())

    n = len(loader)
    r2  = r2_score(all_shi_true, all_shi_pred)
    acc = np.mean(np.array(all_cls_true) == np.array(all_cls_pred))
    return {
        "loss": total_loss / n,
        "reg_loss": reg_loss_sum / n,
        "cls_loss": cls_loss_sum / n,
        "r2": r2,
        "acc": acc,
    }


@torch.no_grad()
def evaluate(model, loader, loss_fn, device):
    model.eval()
    total_loss = reg_loss_sum = cls_loss_sum = 0.0
    all_shi_true, all_shi_pred = [], []
    all_cls_true, all_cls_pred = [], []

    for batch in loader:
        tabular    = batch["tabular"].to(device)
        ts         = batch["ts"].to(device)
        img        = batch["img"].to(device)
        shi_true   = batch["shi"].to(device)
        class_true = batch["soil_class"].to(device)

        shi_pred, logits = model(tabular, ts, img)
        loss, r, c = loss_fn(shi_pred, logits, shi_true, class_true)

        total_loss    += loss.item()
        reg_loss_sum  += r
        cls_loss_sum  += c

        all_shi_true.extend(shi_true.cpu().numpy())
        all_shi_pred.extend(shi_pred.cpu().numpy())
        all_cls_true.extend(class_true.cpu().numpy())
        all_cls_pred.extend(logits.argmax(dim=-1).cpu().numpy())

    n = len(loader)
    r2  = r2_score(all_shi_true, all_shi_pred)
    acc = np.mean(np.array(all_cls_true) == np.array(all_cls_pred))
    return {
        "loss": total_loss / n,
        "reg_loss": reg_loss_sum / n,
        "cls_loss": cls_loss_sum / n,
        "r2": r2,
        "acc": acc,
        "cls_true": np.array(all_cls_true),
        "cls_pred": np.array(all_cls_pred),
        "shi_true": np.array(all_shi_true),
        "shi_pred": np.array(all_shi_pred),
    }


# ─────────────────────────────────────────────────────────
# 4. Main training loop
# ─────────────────────────────────────────────────────────
def train(model, train_loader, val_loader, class_weights,
          device, epochs=60, lr=1e-3, weight_decay=1e-4):
    """
    Training strategy:
      - AdamW: Adam + decoupled weight decay → better regularisation
      - CosineAnnealingLR: smooth LR decay that avoids sharp drops
        (better than StepLR for small datasets)
      - Early stopping on val loss to prevent overfitting
      - Save best checkpoint by val accuracy
    """
    class_weights = class_weights.to(device)
    loss_fn = CombinedLoss(class_weights, gamma=2.0, lambda_cls=1.0)
    optimizer = AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=lr, weight_decay=weight_decay,
    )
    # CosineAnnealingLR: LR goes from lr → 0 over T_max epochs
    # This prevents the model from getting stuck in sharp minima
    scheduler = CosineAnnealingLR(optimizer, T_max=epochs, eta_min=lr * 0.01)

    best_val_acc   = 0.0
    best_val_r2    = -float("inf")
    patience       = 15
    patience_count = 0
    history        = []

    print(f"\n{'Epoch':>5} | {'Train Loss':>10} | {'Train R²':>8} | "
          f"{'Train Acc':>9} | {'Val Loss':>8} | {'Val R²':>7} | {'Val Acc':>7}")
    print("─" * 72)

    for epoch in range(1, epochs + 1):
        t0 = time.time()
        tr = train_one_epoch(model, train_loader, optimizer, loss_fn, device)
        va = evaluate(model, val_loader, loss_fn, device)
        scheduler.step()

        history.append({"epoch": epoch, "train": tr, "val": va})

        print(f"{epoch:>5} | {tr['loss']:>10.4f} | {tr['r2']:>8.3f} | "
              f"{tr['acc']:>9.3f} | {va['loss']:>8.4f} | {va['r2']:>7.3f} | "
              f"{va['acc']:>7.3f}  ({time.time()-t0:.1f}s)")

        # Save best model (by val acc; break ties with R²)
        if va["acc"] > best_val_acc or (
            va["acc"] == best_val_acc and va["r2"] > best_val_r2
        ):
            best_val_acc = va["acc"]
            best_val_r2  = va["r2"]
            torch.save(model.state_dict(), "best_soil_model.pt")
            patience_count = 0
        else:
            patience_count += 1
            if patience_count >= patience:
                print(f"\nEarly stopping at epoch {epoch}")
                break

    print(f"\nBest Val Acc: {best_val_acc:.3f} | Best Val R²: {best_val_r2:.3f}")
    return history


def print_final_report(model, test_loader, class_weights, device):
    """Print classification report and final metrics on test set."""
    class_weights = class_weights.to(device)
    loss_fn = CombinedLoss(class_weights)
    model.load_state_dict(torch.load("best_soil_model.pt", map_location=device))
    results = evaluate(model, test_loader, loss_fn, device)

    print("\n" + "=" * 50)
    print("TEST SET RESULTS")
    print("=" * 50)
    print(f"R²  (SHI regression) : {results['r2']:.4f}")
    print(f"Accuracy (soil class): {results['acc']:.4f}")
    print("\nClassification Report:")
    print(classification_report(
        results["cls_true"], results["cls_pred"],
        target_names=["Poor", "Moderate", "Healthy"]
    ))
    print("Confusion Matrix:")
    print(confusion_matrix(results["cls_true"], results["cls_pred"]))
    return results