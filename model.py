"""
=============================================================
 Multimodal Soil Health Prediction Model
 Architecture: ResNet18 (image) + MLP (tabular) + LSTM (NDVI)
 Fusion: Gated Feature Fusion
=============================================================
"""

import torch
import torch.nn as nn
import torchvision.models as models


# ─────────────────────────────────────────────────────────
# 1. IMAGE BRANCH  →  ResNet18 backbone
# ─────────────────────────────────────────────────────────
class ImageBranch(nn.Module):
    """
    WHY ResNet18?
    - Small dataset (~2200 samples) → deep nets overfit easily
    - ResNet18 pretrained on ImageNet gives strong low-level features
    - We FREEZE early layers and only fine-tune the last block + head
      so that the pretrained spatial features are preserved while
      domain-specific patterns are learned
    """
    def __init__(self, out_dim: int = 128, freeze_backbone: bool = True):
        super().__init__()
        backbone = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

        if freeze_backbone:
            # Freeze all layers except layer4 and fc
            for name, param in backbone.named_parameters():
                if not name.startswith(("layer4", "fc")):
                    param.requires_grad = False

        # Replace the final FC with our projection head
        in_features = backbone.fc.in_features          # 512
        backbone.fc = nn.Sequential(
            nn.Linear(in_features, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(256, out_dim),
        )
        self.backbone = backbone

    def forward(self, x):           # x: (B, 3, H, W)
        return self.backbone(x)     # → (B, out_dim)


# ─────────────────────────────────────────────────────────
# 2. TABULAR BRANCH  →  MLP with BatchNorm + Dropout
# ─────────────────────────────────────────────────────────
class TabularBranch(nn.Module):
    """
    WHY BatchNorm?
    - Normalises activations layer-by-layer → faster convergence
    - Acts as implicit regularizer on small datasets

    WHY increasing then decreasing width?
    - Expand to 256 first to capture cross-feature interactions
    - Compress back to out_dim to force meaningful representation
    """
    def __init__(self, in_dim: int, out_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(in_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),

            nn.Linear(256, 128),
            nn.BatchNorm1d(128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),

            nn.Linear(128, out_dim),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):           # x: (B, in_dim)
        return self.net(x)          # → (B, out_dim)


# ─────────────────────────────────────────────────────────
# 3. TIME-SERIES BRANCH  →  LSTM for NDVI sequences
# ─────────────────────────────────────────────────────────
class NDVIBranch(nn.Module):
    """
    WHY LSTM?
    - NDVI changes over time encode vegetation health trends
    - LSTM captures temporal dependencies (drought → recovery, etc.)
    - Bidirectional: reads past AND future context of the sequence
    - We take the final hidden state as the sequence summary

    WHY NOT Transformer?
    - Only 8 timesteps → Transformer's attention is overkill
    - LSTM is more stable and data-efficient on short sequences
    """
    def __init__(self, input_size: int = 3, hidden_size: int = 64,
                 num_layers: int = 2, out_dim: int = 128):
        super().__init__()
        # input_size=3: ndvi, temp, rain at each timestep
        self.lstm = nn.LSTM(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            batch_first=True,
            bidirectional=True,
            dropout=0.3 if num_layers > 1 else 0.0,
        )
        # bidirectional → hidden_size * 2
        self.proj = nn.Sequential(
            nn.Linear(hidden_size * 2, out_dim),
            nn.ReLU(inplace=True),
        )

    def forward(self, x):                       # x: (B, T, 3)
        out, (h_n, _) = self.lstm(x)
        # Concat forward and backward final hidden states
        h_fwd = h_n[-2]                         # last forward layer
        h_bwd = h_n[-1]                         # last backward layer
        h = torch.cat([h_fwd, h_bwd], dim=-1)   # (B, hidden*2)
        return self.proj(h)                     # → (B, out_dim)


# ─────────────────────────────────────────────────────────
# 4. GATED FUSION  →  Lightweight learned gating
# ─────────────────────────────────────────────────────────
class GatedFusion(nn.Module):
    """
    WHY Gated Fusion instead of plain concatenation?
    - Simple concat treats all modalities equally → wrong
    - When an image is uninformative (e.g., featureless RGB),
      the gate can learn to down-weight it automatically
    - The gate is a sigmoid-activated linear layer → values 0..1
    - Gated output = gate * feature_vector (element-wise)
    - This is MUCH lighter than cross-attention but still adaptive

    FORMULA: z = σ(W [img; tab; ts] + b)
             fused = z ⊙ [img; tab; ts]
    """
    def __init__(self, total_dim: int):
        super().__init__()
        self.gate = nn.Sequential(
            nn.Linear(total_dim, total_dim),
            nn.Sigmoid(),
        )

    def forward(self, *features):
        x = torch.cat(features, dim=-1)    # (B, total_dim)
        g = self.gate(x)                   # (B, total_dim)
        return x * g                       # element-wise gating


# ─────────────────────────────────────────────────────────
# 5. FULL MULTIMODAL MODEL
# ─────────────────────────────────────────────────────────
class SoilHealthModel(nn.Module):
    """
    Complete multimodal model that predicts:
      - soil_health_index  (regression, 0–1)
      - soil_class         (classification: Poor/Moderate/Healthy)

    Inputs:
      - img:      (B, 3, 224, 224)  RGB soil/crop image
      - tabular:  (B, n_tab)        N, P, K, pH, rainfall, temp, humidity, OC, sand
      - ts:       (B, T, 3)         NDVI+temp+rain per timestep

    Design choices:
      - Branch dim = 128 for each modality → total concat = 384
      - Gated fusion → 384 → shared representation
      - Two heads share the fused features
      - Sigmoid on regression head → constrain output to [0,1]
    """
    def __init__(
        self,
        n_tabular_features: int,
        n_timesteps: int = 8,
        branch_dim: int = 128,
        n_classes: int = 3,
        use_image: bool = True,
    ):
        super().__init__()
        self.use_image = use_image

        # Branches
        if use_image:
            self.img_branch = ImageBranch(out_dim=branch_dim)
            total_dim = branch_dim * 3
        else:
            total_dim = branch_dim * 2

        self.tab_branch = TabularBranch(in_dim=n_tabular_features, out_dim=branch_dim)
        self.ts_branch  = NDVIBranch(input_size=3, hidden_size=64, out_dim=branch_dim)

        # Fusion
        self.fusion = GatedFusion(total_dim=total_dim)

        # Shared trunk after fusion
        self.shared = nn.Sequential(
            nn.Linear(total_dim, 256),
            nn.BatchNorm1d(256),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
        )

        # Task heads
        self.regression_head = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, 1),
            nn.Sigmoid(),           # constrain to [0, 1]
        )

        self.classification_head = nn.Sequential(
            nn.Linear(128, 64),
            nn.ReLU(inplace=True),
            nn.Linear(64, n_classes),
            # No softmax here — CrossEntropyLoss expects raw logits
        )

    def forward(self, tabular, ts, img=None):
        tab_feat = self.tab_branch(tabular)     # (B, 128)
        ts_feat  = self.ts_branch(ts)           # (B, 128)

        if self.use_image and img is not None:
            img_feat = self.img_branch(img)     # (B, 128)
            fused = self.fusion(img_feat, tab_feat, ts_feat)
        else:
            fused = self.fusion(tab_feat, ts_feat)

        shared = self.shared(fused)             # (B, 128)

        shi    = self.regression_head(shared).squeeze(-1)   # (B,)
        logits = self.classification_head(shared)           # (B, n_classes)

        return shi, logits