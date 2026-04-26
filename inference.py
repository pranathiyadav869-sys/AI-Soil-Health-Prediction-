"""
=============================================================
 Inference Pipeline
 Single entry point that:
   1. Loads trained model + scalers
   2. Runs model inference (SHI + soil class)
   3. Runs decision support layer
   4. Returns structured JSON output
=============================================================
"""

import numpy as np
import torch
import pickle
import json
from model import SoilHealthModel
from dataset import TABULAR_COLS, NDVI_COLS, TEMP_COLS, RAIN_COLS
from decision_support import SoilProfile, generate_full_report, print_report

SOIL_CLASS_MAP = {0: "Poor", 1: "Moderate", 2: "Healthy"}


class SoilHealthPredictor:
    """
    Production inference class.
    Load once, call predict() many times.
    """

    def __init__(self, model_path: str, scaler_path: str, device: str = "cpu"):
        self.device = torch.device(device)

        # Load scalers
        with open(scaler_path, "rb") as f:
            scalers = pickle.load(f)
        self.tab_scaler = scalers["tab_scaler"]
        self.ts_scaler  = scalers["ts_scaler"]
        self.n_tab      = len(TABULAR_COLS)

        # Load model
        self.model = SoilHealthModel(
            n_tabular_features=self.n_tab,
            n_timesteps=8,
            branch_dim=128,
            n_classes=3,
            use_image=True,
        )
        self.model.load_state_dict(
            torch.load(model_path, map_location=self.device)
        )
        self.model.eval()
        self.model.to(self.device)

    @torch.no_grad()
    def predict(
        self,
        N: float, P: float, K: float, pH: float,
        rainfall: float, temperature: float, humidity: float,
        organic_carbon: float, sand: float,
        ndvi_sequence: list,       # list of 8 NDVI values
        temp_sequence: list,       # list of 8 temperature values
        rain_sequence: list,       # list of 8 rainfall values
        image_tensor=None,         # (3, 224, 224) torch tensor or None
    ) -> dict:
        """
        Run end-to-end prediction + recommendations.

        Parameters
        ----------
        ndvi_sequence : list of 8 floats (NDVI at 8 time points)
        temp_sequence : list of 8 floats (temperature at 8 time points)
        rain_sequence : list of 8 floats (rainfall at 8 time points)
        image_tensor  : optional (3, 224, 224) float tensor

        Returns
        -------
        Full JSON-serialisable report dict
        """
        # ── Prepare tabular ──────────────────────────────────────
        tab_raw = np.array([[N, P, K, pH, rainfall, temperature,
                             humidity, organic_carbon, sand]], dtype=np.float32)
        tab_scaled = self.tab_scaler.transform(tab_raw)
        tab_tensor = torch.tensor(tab_scaled, dtype=torch.float32).to(self.device)

        # ── Prepare time-series ──────────────────────────────────
        ts_raw = np.array(
            [[ndvi_sequence, temp_sequence, rain_sequence]],
            dtype=np.float32,
        )  # (1, 3, 8) → need (1, 8, 3)
        ts_raw = ts_raw.transpose(0, 2, 1)   # → (1, 8, 3)
        ts_flat = ts_raw.reshape(-1, 3)
        ts_scaled = self.ts_scaler.transform(ts_flat)
        ts_raw = ts_scaled.reshape(1, 8, 3)
        ts_tensor = torch.tensor(ts_raw, dtype=torch.float32).to(self.device)

        # ── Prepare image ────────────────────────────────────────
        if image_tensor is None:
            img_tensor = torch.zeros(1, 3, 224, 224).to(self.device)
        else:
            img_tensor = image_tensor.unsqueeze(0).to(self.device)

        # ── Model inference ──────────────────────────────────────
        shi_pred, logits = self.model(tab_tensor, ts_tensor, img_tensor)
        shi_value   = float(shi_pred[0].item())
        class_idx   = int(logits[0].argmax().item())
        soil_class  = SOIL_CLASS_MAP[class_idx]
        class_probs = torch.softmax(logits[0], dim=0).cpu().numpy().tolist()

        # ── Decision support ─────────────────────────────────────
        profile = SoilProfile(
            N=N, P=P, K=K, pH=pH,
            rainfall=rainfall, temperature=temperature,
            humidity=humidity, organic_carbon=organic_carbon, sand=sand,
            shi=shi_value, soil_class=soil_class,
        )
        report = generate_full_report(profile)

        # Inject model confidence
        report["model_confidence"] = {
            "class_probabilities": {
                "Poor": round(class_probs[0], 4),
                "Moderate": round(class_probs[1], 4),
                "Healthy": round(class_probs[2], 4),
            }
        }

        return report


# ─────────────────────────────────────────────────────────
# Quick demo (no trained model needed — uses random weights)
# ─────────────────────────────────────────────────────────
def demo_decision_support_only():
    """
    Demonstrate the decision support layer independently
    (no model checkpoint required).
    """
    from decision_support import SoilProfile, generate_full_report, print_report

    # Example: sandy, slightly acidic, low-N soil in a warm humid region
    profile = SoilProfile(
        N=25, P=45, K=80, pH=5.8,
        rainfall=120, temperature=28, humidity=65,
        organic_carbon=4.2, sand=72,
        shi=0.38,       # ← from model prediction
        soil_class="Moderate",
    )

    report = generate_full_report(profile)
    print_report(report)
    print("\n── JSON OUTPUT ──")
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    print("Running decision support demo (no model checkpoint needed)...")
    demo_decision_support_only()