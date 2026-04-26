"""
=============================================================
 run_training.py
 Full training pipeline — run this to train the model
=============================================================

Usage:
    python run_training.py --csv path/to/final_dataset_with_ndvi_weather.csv

Requirements:
    pip install torch torchvision scikit-learn pandas numpy
"""

import argparse
import pickle
import torch
from dataset import build_dataloaders
from model import SoilHealthModel
from train import train, print_final_report


def main(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # ── 1. Data ──────────────────────────────────────────────────
    train_loader, val_loader, test_loader, train_ds, class_weights = \
        build_dataloaders(
            csv_path=args.csv,
            batch_size=args.batch_size,
        )

    # Save scalers for inference
    with open("scalers.pkl", "wb") as f:
        pickle.dump({
            "tab_scaler": train_ds.tab_scaler,
            "ts_scaler":  train_ds.ts_scaler,
        }, f)
    print("Scalers saved to scalers.pkl")

    # ── 2. Model ─────────────────────────────────────────────────
    model = SoilHealthModel(
        n_tabular_features=len(train_ds.tabular[0]),
        n_timesteps=8,
        branch_dim=128,
        n_classes=3,
        use_image=True,   # set False if no real images available
    ).to(device)

    n_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Trainable parameters: {n_params:,}")

    # ── 3. Training ──────────────────────────────────────────────
    history = train(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        class_weights=class_weights,
        device=device,
        epochs=args.epochs,
        lr=args.lr,
        weight_decay=args.weight_decay,
    )

    # ── 4. Evaluation ────────────────────────────────────────────
    print_final_report(model, test_loader, class_weights, device)
    print("\nModel saved to best_soil_model.pt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv",          type=str,   required=True)
    parser.add_argument("--batch_size",   type=int,   default=32)
    parser.add_argument("--epochs",       type=int,   default=60)
    parser.add_argument("--lr",           type=float, default=1e-3)
    parser.add_argument("--weight_decay", type=float, default=1e-4)
    args = parser.parse_args()
    main(args)