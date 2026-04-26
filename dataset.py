"""
=============================================================
 Dataset + Data Utilities for Soil Health Prediction
=============================================================
"""

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader, WeightedRandomSampler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split


# ─────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────
TABULAR_COLS = [
    "N", "P", "K", "ph", "rainfall",
    "temperature", "humidity", "organic_carbon", "sand",
]

NDVI_COLS  = [f"ndvi_t{i}" for i in range(1, 9)]
TEMP_COLS  = [f"temp_t{i}" for i in range(1, 9)]
RAIN_COLS  = [f"rain_t{i}" for i in range(1, 9)]

# Soil health thresholds — adjust these based on domain knowledge
SHI_THRESHOLDS = {"poor": 0.35, "moderate": 0.50}

SOIL_CLASS_LABELS = {0: "Poor", 1: "Moderate", 2: "Healthy"}


def shi_to_class(shi_value: float) -> int:
    """Convert continuous SHI to 3-class label."""
    if shi_value < SHI_THRESHOLDS["poor"]:
        return 0   # Poor
    elif shi_value < SHI_THRESHOLDS["moderate"]:
        return 1   # Moderate
    else:
        return 2   # Healthy


# ─────────────────────────────────────────────────────────
# Dataset
# ─────────────────────────────────────────────────────────
class SoilDataset(Dataset):
    """
    Handles three data modalities:
      1. tabular  – static soil/weather features
      2. ts       – (T, 3) time-series: NDVI + temp + rain per step
      3. img      – optional; returns dummy tensor when no real images

    WHY normalise per-scaler?
    - Tabular features have very different ranges (N: 0–140, pH: 3–9)
    - Standardisation prevents large-scale features dominating gradients
    - NDVI is already in [-1, 1] but we standardise anyway for consistency
    """

    def __init__(self, df: pd.DataFrame, tab_scaler=None,
                 ts_scaler=None, fit_scalers=False):
        self.df = df.reset_index(drop=True)

        # ---------- Build tabular tensor ----------
        tab = df[TABULAR_COLS].values.astype(np.float32)
        if fit_scalers:
            self.tab_scaler = StandardScaler()
            tab = self.tab_scaler.fit_transform(tab)
        else:
            self.tab_scaler = tab_scaler
            tab = tab_scaler.transform(tab)
        self.tabular = torch.tensor(tab, dtype=torch.float32)

        # ---------- Build time-series tensor ----------
        ndvi  = df[NDVI_COLS].values.astype(np.float32)   # (N, 8)
        temps = df[TEMP_COLS].values.astype(np.float32)
        rains = df[RAIN_COLS].values.astype(np.float32)
        ts_raw = np.stack([ndvi, temps, rains], axis=-1)  # (N, 8, 3)

        if fit_scalers:
            N, T, C = ts_raw.shape
            self.ts_scaler = StandardScaler()
            ts_flat = ts_raw.reshape(-1, C)
            ts_flat = self.ts_scaler.fit_transform(ts_flat)
            ts_raw = ts_flat.reshape(N, T, C)
        else:
            self.ts_scaler = ts_scaler
            N, T, C = ts_raw.shape
            ts_flat = ts_raw.reshape(-1, C)
            ts_flat = ts_scaler.transform(ts_flat)
            ts_raw = ts_flat.reshape(N, T, C)

        self.ts = torch.tensor(ts_raw, dtype=torch.float32)

        # ---------- Labels ----------
        shi = df["soil_health_index"].values.astype(np.float32)
        self.shi = torch.tensor(shi, dtype=torch.float32)
        self.soil_class = torch.tensor(
            [shi_to_class(v) for v in shi], dtype=torch.long
        )

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        # Dummy image: replace with real image loading if images available
        dummy_img = torch.zeros(3, 224, 224)
        return {
            "tabular":    self.tabular[idx],
            "ts":         self.ts[idx],
            "img":        dummy_img,
            "shi":        self.shi[idx],
            "soil_class": self.soil_class[idx],
        }


# ─────────────────────────────────────────────────────────
# Build DataLoaders
# ─────────────────────────────────────────────────────────
def build_dataloaders(csv_path: str, batch_size: int = 32,
                      val_size: float = 0.15, test_size: float = 0.15,
                      seed: int = 42):
    """
    Returns train/val/test DataLoaders + fitted scalers + class weights.

    WHY WeightedRandomSampler?
    - After applying SHI thresholds the classes may be imbalanced
    - The sampler over-samples minority classes so the model sees
      them more frequently → fixes the 'Poor class issue'
    - We compute inverse-frequency weights per sample
    """
    df = pd.read_csv("/Users/pranathi15/Desktop/soil_health_project/final_dataset_with_ndvi_weather.csv")

    # Split before scaling to prevent data leakage
    df_trainval, df_test = train_test_split(
        df, test_size=test_size, random_state=seed
    )
    df_train, df_val = train_test_split(
        df_trainval,
        test_size=val_size / (1 - test_size),
        random_state=seed,
    )

    # Fit scalers on train only
    train_ds = SoilDataset(df_train, fit_scalers=True)
    val_ds   = SoilDataset(df_val,
                           tab_scaler=train_ds.tab_scaler,
                           ts_scaler=train_ds.ts_scaler)
    test_ds  = SoilDataset(df_test,
                           tab_scaler=train_ds.tab_scaler,
                           ts_scaler=train_ds.ts_scaler)

    # Compute per-class weights for loss function
    class_counts = torch.bincount(train_ds.soil_class)
    class_weights = 1.0 / class_counts.float()
    class_weights = class_weights / class_weights.sum()   # normalise

    # Per-sample weights for WeightedRandomSampler
    sample_weights = class_weights[train_ds.soil_class]

    sampler = WeightedRandomSampler(
        weights=sample_weights,
        num_samples=len(train_ds),
        replacement=True,
    )

    train_loader = DataLoader(train_ds, batch_size=batch_size,
                              sampler=sampler, num_workers=2, pin_memory=True)
    val_loader   = DataLoader(val_ds,   batch_size=batch_size,
                              shuffle=False, num_workers=2, pin_memory=True)
    test_loader  = DataLoader(test_ds,  batch_size=batch_size,
                              shuffle=False, num_workers=2, pin_memory=True)

    print(f"Dataset split  →  Train: {len(train_ds)} | Val: {len(val_ds)} | Test: {len(test_ds)}")
    print(f"Class distribution (train): {dict(zip(['Poor','Moderate','Healthy'], class_counts.tolist()))}")
    print(f"Class weights: {class_weights.tolist()}")

    return train_loader, val_loader, test_loader, train_ds, class_weights