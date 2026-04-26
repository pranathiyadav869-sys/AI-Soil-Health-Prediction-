# """
# =============================================================
#  image_inference.py
 
#  Drop-in image analysis module for your existing Gradio app.
 
#  USAGE:
#    from image_inference import SoilImageAnalyzer
#    analyzer = SoilImageAnalyzer("soil_image_model.pt", "soil_image_labels.json")
#    result = analyzer.analyze(pil_image_or_numpy_array)
#    print(result["explanation"])

#  PLACE THIS FILE in your VS Code project alongside app.py
# =============================================================
# """

# import json
# import numpy as np
# import torch
# import torch.nn as nn
# import torchvision.models as models
# import torchvision.transforms as T
# from PIL import Image

# # ── Label constants (must match training) ─────────────
# SOIL_TYPES           = ["Clay", "Sandy", "Loamy", "Black", "Red", "Alluvial"]
# MOISTURE_LABELS      = ["Dry", "Moist", "Wet"]
# VEGETATION_LABELS    = ["Low", "Medium", "High"]
# CROP_CONDITION_LABELS= ["Healthy", "Unhealthy"]
# DISEASE_LABELS       = [
#     "Healthy", "Bacterial_Spot", "Early_Blight", "Late_Blight",
#     "Leaf_Mold", "Septoria_Leaf_Spot", "Spider_Mites",
#     "Target_Spot", "Yellow_Leaf_Curl", "Mosaic_Virus", "Powdery_Mildew",
# ]

# # ── Image preprocessing (must match training) ─────────
# INFERENCE_TRANSFORMS = T.Compose([
#     T.Resize((224, 224)),
#     T.ToTensor(),
#     T.Normalize(mean=[0.485, 0.456, 0.406],
#                 std=[0.229, 0.224, 0.225]),
# ])

# BRANCH_DIM = 256  # must match training config


# # ─────────────────────────────────────────────────────
# # Model (same architecture as training)
# # ─────────────────────────────────────────────────────
# class SoilImageCNN(nn.Module):
#     def __init__(self):
#         super().__init__()
#         backbone = models.resnet18(weights=None)  # no pretrained needed at inference
#         self.feature_extractor = nn.Sequential(*list(backbone.children())[:-1])

#         self.shared_proj = nn.Sequential(
#             nn.Linear(512, BRANCH_DIM),
#             nn.BatchNorm1d(BRANCH_DIM),
#             nn.ReLU(inplace=True),
#             nn.Dropout(0.4),
#         )
#         self.head_soil_type      = self._make_head(len(SOIL_TYPES))
#         self.head_moisture       = self._make_head(len(MOISTURE_LABELS))
#         self.head_vegetation     = self._make_head(len(VEGETATION_LABELS))
#         self.head_crop_condition = self._make_head(len(CROP_CONDITION_LABELS))
#         self.head_disease        = self._make_head(len(DISEASE_LABELS))

#     def _make_head(self, n_classes):
#         return nn.Sequential(
#             nn.Linear(BRANCH_DIM, 128),
#             nn.ReLU(inplace=True),
#             nn.Dropout(0.3),
#             nn.Linear(128, n_classes),
#         )

#     def forward(self, x):
#         feats  = self.feature_extractor(x).flatten(1)
#         shared = self.shared_proj(feats)
#         return {
#             "soil_type":      self.head_soil_type(shared),
#             "moisture":       self.head_moisture(shared),
#             "vegetation":     self.head_vegetation(shared),
#             "crop_condition": self.head_crop_condition(shared),
#             "disease":        self.head_disease(shared),
#         }


# # ─────────────────────────────────────────────────────
# # Natural Language Generator
# # ─────────────────────────────────────────────────────
# def generate_explanation(pred: dict) -> str:
#     """
#     Convert structured predictions into a human-readable
#     agronomic explanation.

#     WHY RULE-BASED NLG?
#     ─────────────────────────────────────────────────────
#     - The explanation must be trustworthy and auditable
#     - Field extension workers need to verify the logic
#     - Template-based generation ensures consistent phrasing
#     - Each clause is grounded in agronomic domain knowledge
#     """
#     soil   = pred["soil_type"]
#     moist  = pred["moisture"]
#     veg    = pred["vegetation"]
#     cond   = pred["crop_condition"]
#     disease= pred["disease"]

#     # ── Soil description ──────────────────────────────
#     soil_desc = {
#         "Clay":     "heavy clay soil with high water retention",
#         "Sandy":    "light sandy soil with low water retention and fast drainage",
#         "Loamy":    "well-balanced loamy soil with good fertility",
#         "Black":    "black (regur) soil rich in calcium and magnesium",
#         "Red":      "red laterite soil typically low in nitrogen",
#         "Alluvial": "alluvial soil with high agricultural productivity",
#     }.get(soil, soil)

#     # ── Moisture description ──────────────────────────
#     moisture_desc = {
#         "Dry":   "moisture levels appear critically low",
#         "Moist": "moisture levels appear adequate",
#         "Wet":   "moisture levels appear high — possible waterlogging risk",
#     }.get(moist, moist)

#     # ── Vegetation description ────────────────────────
#     veg_desc = {
#         "Low":    "very little vegetation or crop cover is visible",
#         "Medium": "moderate vegetation or crop coverage is present",
#         "High":   "dense vegetation or healthy crop coverage is visible",
#     }.get(veg, veg)

#     # ── Crop condition description ────────────────────
#     cond_desc = {
#         "Healthy":   "Crop condition appears healthy.",
#         "Unhealthy": "Crops appear stressed or unhealthy.",
#     }.get(cond, cond)

#     # ── Disease description ───────────────────────────
#     if disease == "Healthy":
#         disease_desc = "No visible disease indicators were detected."
#     else:
#         disease_name = disease.replace("_", " ")
#         disease_desc = (f"Possible {disease_name} detected. "
#                         "Consult an agronomist and consider targeted treatment.")

#     # ── Recommendations ───────────────────────────────
#     recommendations = []

#     if moist == "Dry" and soil in ("Sandy", "Red"):
#         recommendations.append(
#             "Immediate irrigation is recommended — sandy/red soils dry out quickly."
#         )
#     if moist == "Wet" and soil == "Clay":
#         recommendations.append(
#             "Improve drainage to prevent root rot — clay soil retains excess water."
#         )
#     if veg == "Low":
#         recommendations.append(
#             "Consider mulching or cover cropping to protect bare soil from erosion."
#         )
#     if cond == "Unhealthy" or disease != "Healthy":
#         recommendations.append(
#             "Conduct a detailed field inspection and soil nutrient test."
#         )

#     rec_str = (" ".join(recommendations) if recommendations
#                else "Maintain current farming practices.")

#     explanation = (
#         f"The image shows {soil_desc}. "
#         f"Visually, {moisture_desc}. "
#         f"Additionally, {veg_desc}. "
#         f"{cond_desc} "
#         f"{disease_desc} "
#         f"Recommendation: {rec_str}"
#     )

#     return explanation


# def generate_html_output(pred: dict, confs: dict, explanation: str) -> str:
#     """Generate styled HTML card for Gradio display."""

#     def confidence_bar(pct, color="steelblue"):
#         return (f'<div style="background:#eee;border-radius:4px;height:12px;width:100%">'
#                 f'<div style="background:{color};width:{pct:.0f}%;height:12px;'
#                 f'border-radius:4px"></div></div>')

#     cond_color = "#e6ffe6" if pred["crop_condition"] == "Healthy" else "#ffe6e6"
#     dis_color  = "#e6ffe6" if pred["disease"] == "Healthy" else "#fff3cd"

#     html = f"""
# <div style="font-family:Arial,sans-serif;padding:16px;border-radius:12px;
#             background:#f9f9f9;border:1px solid #ddd;max-width:700px">

#   <h2 style="color:#2e7d32;margin-top:0">🌱 Soil & Crop Image Analysis</h2>

#   <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">

#     <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
#       <b>🪨 Soil Type</b>
#       <p style="font-size:1.2em;margin:4px 0;color:#1565C0">{pred["soil_type"]}</p>
#       {confidence_bar(confs["soil_type"]*100, "#1565C0")}
#       <small>{confs["soil_type"]*100:.1f}% confidence</small>
#     </div>

#     <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
#       <b>💧 Moisture</b>
#       <p style="font-size:1.2em;margin:4px 0;color:#0277BD">{pred["moisture"]}</p>
#       {confidence_bar(confs["moisture"]*100, "#0277BD")}
#       <small>{confs["moisture"]*100:.1f}% confidence</small>
#     </div>

#     <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
#       <b>🌿 Vegetation</b>
#       <p style="font-size:1.2em;margin:4px 0;color:#388E3C">{pred["vegetation"]}</p>
#       {confidence_bar(confs["vegetation"]*100, "#388E3C")}
#       <small>{confs["vegetation"]*100:.1f}% confidence</small>
#     </div>

#     <div style="background:{cond_color};padding:12px;border-radius:8px;border:1px solid #eee">
#       <b>🌾 Crop Condition</b>
#       <p style="font-size:1.2em;margin:4px 0">{pred["crop_condition"]}</p>
#       {confidence_bar(confs["crop_condition"]*100, "#43A047")}
#       <small>{confs["crop_condition"]*100:.1f}% confidence</small>
#     </div>

#   </div>

#   <div style="background:{dis_color};padding:12px;border-radius:8px;
#               border:1px solid #eee;margin-bottom:16px">
#     <b>🦠 Disease Indicator</b>
#     <p style="font-size:1.1em;margin:4px 0">{pred["disease"].replace("_"," ")}</p>
#     {confidence_bar(confs["disease"]*100, "#E53935")}
#     <small>{confs["disease"]*100:.1f}% confidence</small>
#   </div>

#   <div style="background:#E8F5E9;padding:14px;border-radius:8px;border-left:4px solid #2e7d32">
#     <b>📋 Expert Explanation</b>
#     <p style="margin:8px 0;line-height:1.6">{explanation}</p>
#   </div>

# </div>
# """
#     return html


# # ─────────────────────────────────────────────────────
# # Main Analyzer Class
# # ─────────────────────────────────────────────────────
# class SoilImageAnalyzer:
#     """
#     Load once at app startup, call analyze() per request.

#     Parameters
#     ----------
#     model_path : str   path to soil_image_model.pt
#     label_path : str   path to soil_image_labels.json (optional)
#     device     : str   'cpu' or 'cuda'
#     """

#     def __init__(self, model_path: str,
#                  label_path: str = None,
#                  device: str = "cpu"):
#         self.device = torch.device(device)

#         # Load model
#         self.model = SoilImageCNN()

#     try:
#         print("🔄 Loading model from:", model_path)
#         state = torch.load(model_path, map_location=self.device)
#         self.model.load_state_dict(state, strict=False)

#         self.model.eval()
#         self.model.to(self.device)

#         print("✅ Model loaded successfully")

#     except Exception as e:
#         print("❌ MODEL LOAD ERROR:", e)

#         # Load label config if provided
#         if label_path:
#             with open(label_path) as f:
#                 self.label_config = json.load(f)
#         else:
#             self.label_config = None

#     @torch.no_grad()
#     def analyze(self, image) -> dict:
#         """
#         Analyze a soil/crop image.

#         Parameters
#         ----------
#         image : PIL.Image, numpy.ndarray, or file path (str)

#         Returns
#         -------
#         dict with keys:
#           predictions  – {soil_type, moisture, vegetation, crop_condition, disease}
#           confidences  – confidence scores per task
#           explanation  – human-readable string
#           html         – styled HTML for Gradio display
#         """
#         # ── Preprocess ───────────────────────────────
#         if image is None:
#             return self._empty_result()

#         if isinstance(image, str):
#             pil_img = Image.open(image).convert("RGB")
#         elif isinstance(image, np.ndarray):
#             pil_img = Image.fromarray(image.astype(np.uint8)).convert("RGB")
#         elif isinstance(image, Image.Image):
#             pil_img = image.convert("RGB")
#         else:
#             pil_img = Image.fromarray(image).convert("RGB")

#         tensor = INFERENCE_TRANSFORMS(pil_img).unsqueeze(0).to(self.device)

#         # ── Inference ────────────────────────────────
#         outputs = self.model(tensor)

#         # ── Decode predictions + confidences ─────────
#         label_maps = {
#             "soil_type":      SOIL_TYPES,
#             "moisture":       MOISTURE_LABELS,
#             "vegetation":     VEGETATION_LABELS,
#             "crop_condition": CROP_CONDITION_LABELS,
#             "disease":        DISEASE_LABELS,
#         }

#         predictions  = {}
#         confidences  = {}
#         all_probs    = {}

#         for task, logits in outputs.items():
#             probs    = torch.softmax(logits[0], dim=0).cpu().numpy()
#             best_idx = int(probs.argmax())
#             labels   = label_maps[task]
#             predictions[task] = labels[best_idx]
#             confidences[task] = float(probs[best_idx])
#             all_probs[task]   = {labels[i]: float(probs[i])
#                                  for i in range(len(labels))}

#         # ── Generate explanation ──────────────────────
#         explanation = generate_explanation(predictions)
#         html        = generate_html_output(predictions, confidences, explanation)

#         return {
#             "predictions":  predictions,
#             "confidences":  confidences,
#             "all_probs":    all_probs,
#             "explanation":  explanation,
#             "html":         html,
#         }

#     def _empty_result(self) -> dict:
#         return {
#             "predictions":  {},
#             "confidences":  {},
#             "all_probs":    {},
#             "explanation":  "No image provided. Please upload a soil or crop image.",
#             "html":         "<p>📸 No image uploaded.</p>",
#         }

#     def get_image_tensor_for_multimodal(self, image) -> torch.Tensor:
#         """
#         Returns a (3, 224, 224) tensor suitable for passing into
#         your existing SoilHealthModel's image branch.

#         Use this in your inference pipeline to replace the dummy_img.
#         """
#         if image is None:
#             return torch.zeros(3, 224, 224)

#         if isinstance(image, np.ndarray):
#             pil_img = Image.fromarray(image.astype(np.uint8)).convert("RGB")
#         elif isinstance(image, Image.Image):
#             pil_img = image.convert("RGB")
#         else:
#             pil_img = Image.open(image).convert("RGB")
"""
=============================================================
 image_inference.py
 
 Drop-in image analysis module for your existing Gradio app.
 
 USAGE:
   from image_inference import SoilImageAnalyzer
   analyzer = SoilImageAnalyzer("soil_image_model.pt", "soil_image_labels.json")
   result = analyzer.analyze(pil_image_or_numpy_array)
   print(result["explanation"])

 PLACE THIS FILE in your VS Code project alongside app.py
=============================================================
"""

import json
import numpy as np
import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from PIL import Image

# ── Label constants (must match training) ─────────────
SOIL_TYPES           = ["Clay", "Sandy", "Loamy", "Black", "Red", "Alluvial"]
MOISTURE_LABELS      = ["Dry", "Moist", "Wet"]
VEGETATION_LABELS    = ["Low", "Medium", "High"]
CROP_CONDITION_LABELS= ["Healthy", "Unhealthy"]
DISEASE_LABELS       = [
    "Healthy", "Bacterial_Spot", "Early_Blight", "Late_Blight",
    "Leaf_Mold", "Septoria_Leaf_Spot", "Spider_Mites",
    "Target_Spot", "Yellow_Leaf_Curl", "Mosaic_Virus", "Powdery_Mildew",
]

# ── Image preprocessing (must match training) ─────────
INFERENCE_TRANSFORMS = T.Compose([
    T.Resize((224, 224)),
    T.ToTensor(),
    T.Normalize(mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]),
])

BRANCH_DIM = 256  # must match training config


# ─────────────────────────────────────────────────────
# Model (same architecture as training)
# ─────────────────────────────────────────────────────
class SoilImageCNN(nn.Module):
    def __init__(self):
        super().__init__()
        backbone = models.resnet18(weights=None)  # no pretrained needed at inference
        self.feature_extractor = nn.Sequential(*list(backbone.children())[:-1])

        self.shared_proj = nn.Sequential(
            nn.Linear(512, BRANCH_DIM),
            nn.BatchNorm1d(BRANCH_DIM),
            nn.ReLU(inplace=True),
            nn.Dropout(0.4),
        )
        self.head_soil_type      = self._make_head(len(SOIL_TYPES))
        self.head_moisture       = self._make_head(len(MOISTURE_LABELS))
        self.head_vegetation     = self._make_head(len(VEGETATION_LABELS))
        self.head_crop_condition = self._make_head(len(CROP_CONDITION_LABELS))
        self.head_disease        = self._make_head(len(DISEASE_LABELS))

    def _make_head(self, n_classes):
        return nn.Sequential(
            nn.Linear(BRANCH_DIM, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(0.3),
            nn.Linear(128, n_classes),
        )

    def forward(self, x):
        feats  = self.feature_extractor(x).flatten(1)
        shared = self.shared_proj(feats)
        return {
            "soil_type":      self.head_soil_type(shared),
            "moisture":       self.head_moisture(shared),
            "vegetation":     self.head_vegetation(shared),
            "crop_condition": self.head_crop_condition(shared),
            "disease":        self.head_disease(shared),
        }


# ─────────────────────────────────────────────────────
# Natural Language Generator
# ─────────────────────────────────────────────────────
def generate_explanation(pred: dict) -> str:
    """
    Convert structured predictions into a human-readable
    agronomic explanation.

    WHY RULE-BASED NLG?
    ─────────────────────────────────────────────────────
    - The explanation must be trustworthy and auditable
    - Field extension workers need to verify the logic
    - Template-based generation ensures consistent phrasing
    - Each clause is grounded in agronomic domain knowledge
    """
    soil   = pred["soil_type"]
    moist  = pred["moisture"]
    veg    = pred["vegetation"]
    cond   = pred["crop_condition"]
    disease= pred["disease"]

    # ── Soil description ──────────────────────────────
    soil_desc = {
        "Clay":     "heavy clay soil with high water retention",
        "Sandy":    "light sandy soil with low water retention and fast drainage",
        "Loamy":    "well-balanced loamy soil with good fertility",
        "Black":    "black (regur) soil rich in calcium and magnesium",
        "Red":      "red laterite soil typically low in nitrogen",
        "Alluvial": "alluvial soil with high agricultural productivity",
    }.get(soil, soil)

    # ── Moisture description ──────────────────────────
    moisture_desc = {
        "Dry":   "moisture levels appear critically low",
        "Moist": "moisture levels appear adequate",
        "Wet":   "moisture levels appear high — possible waterlogging risk",
    }.get(moist, moist)

    # ── Vegetation description ────────────────────────
    veg_desc = {
        "Low":    "very little vegetation or crop cover is visible",
        "Medium": "moderate vegetation or crop coverage is present",
        "High":   "dense vegetation or healthy crop coverage is visible",
    }.get(veg, veg)

    # ── Crop condition description ────────────────────
    cond_desc = {
        "Healthy":   "Crop condition appears healthy.",
        "Unhealthy": "Crops appear stressed or unhealthy.",
    }.get(cond, cond)

    # ── Disease description ───────────────────────────
    if disease == "Healthy":
        disease_desc = "No visible disease indicators were detected."
    else:
        disease_name = disease.replace("_", " ")
        disease_desc = (f"Possible {disease_name} detected. "
                        "Consult an agronomist and consider targeted treatment.")

    # ── Recommendations ───────────────────────────────
    recommendations = []

    if moist == "Dry" and soil in ("Sandy", "Red"):
        recommendations.append(
            "Immediate irrigation is recommended — sandy/red soils dry out quickly."
        )
    if moist == "Wet" and soil == "Clay":
        recommendations.append(
            "Improve drainage to prevent root rot — clay soil retains excess water."
        )
    if veg == "Low":
        recommendations.append(
            "Consider mulching or cover cropping to protect bare soil from erosion."
        )
    if cond == "Unhealthy" or disease != "Healthy":
        recommendations.append(
            "Conduct a detailed field inspection and soil nutrient test."
        )

    rec_str = (" ".join(recommendations) if recommendations
               else "Maintain current farming practices.")

    explanation = (
        f"The image shows {soil_desc}. "
        f"Visually, {moisture_desc}. "
        f"Additionally, {veg_desc}. "
        f"{cond_desc} "
        f"{disease_desc} "
        f"Recommendation: {rec_str}"
    )

    return explanation


def generate_html_output(pred: dict, confs: dict, explanation: str) -> str:
    """Generate styled HTML card for Gradio display."""

    def confidence_bar(pct, color="steelblue"):
        return (f'<div style="background:#eee;border-radius:4px;height:12px;width:100%">'
                f'<div style="background:{color};width:{pct:.0f}%;height:12px;'
                f'border-radius:4px"></div></div>')

    cond_color = "#e6ffe6" if pred["crop_condition"] == "Healthy" else "#ffe6e6"
    dis_color  = "#e6ffe6" if pred["disease"] == "Healthy" else "#fff3cd"

    html = f"""
<div style="font-family:Arial,sans-serif;padding:16px;border-radius:12px;
            background:#f9f9f9;border:1px solid #ddd;max-width:700px">

  <h2 style="color:#2e7d32;margin-top:0">🌱 Soil & Crop Image Analysis</h2>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px">

    <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
      <b>🪨 Soil Type</b>
      <p style="font-size:1.2em;margin:4px 0;color:#1565C0">{pred["soil_type"]}</p>
      {confidence_bar(confs["soil_type"]*100, "#1565C0")}
      <small>{confs["soil_type"]*100:.1f}% confidence</small>
    </div>

    <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
      <b>💧 Moisture</b>
      <p style="font-size:1.2em;margin:4px 0;color:#0277BD">{pred["moisture"]}</p>
      {confidence_bar(confs["moisture"]*100, "#0277BD")}
      <small>{confs["moisture"]*100:.1f}% confidence</small>
    </div>

    <div style="background:#fff;padding:12px;border-radius:8px;border:1px solid #eee">
      <b>🌿 Vegetation</b>
      <p style="font-size:1.2em;margin:4px 0;color:#388E3C">{pred["vegetation"]}</p>
      {confidence_bar(confs["vegetation"]*100, "#388E3C")}
      <small>{confs["vegetation"]*100:.1f}% confidence</small>
    </div>

    <div style="background:{cond_color};padding:12px;border-radius:8px;border:1px solid #eee">
      <b>🌾 Crop Condition</b>
      <p style="font-size:1.2em;margin:4px 0">{pred["crop_condition"]}</p>
      {confidence_bar(confs["crop_condition"]*100, "#43A047")}
      <small>{confs["crop_condition"]*100:.1f}% confidence</small>
    </div>

  </div>

  <div style="background:{dis_color};padding:12px;border-radius:8px;
              border:1px solid #eee;margin-bottom:16px">
    <b>🦠 Disease Indicator</b>
    <p style="font-size:1.1em;margin:4px 0">{pred["disease"].replace("_"," ")}</p>
    {confidence_bar(confs["disease"]*100, "#E53935")}
    <small>{confs["disease"]*100:.1f}% confidence</small>
  </div>

  <div style="background:#E8F5E9;padding:14px;border-radius:8px;border-left:4px solid #2e7d32">
    <b>📋 Expert Explanation</b>
    <p style="margin:8px 0;line-height:1.6">{explanation}</p>
  </div>

</div>
"""
    return html


# ─────────────────────────────────────────────────────
# Main Analyzer Class
# ─────────────────────────────────────────────────────
class SoilImageAnalyzer:
    """
    Load once at app startup, call analyze() per request.

    Parameters
    ----------
    model_path : str   path to soil_image_model.pt
    label_path : str   path to soil_image_labels.json (optional)
    device     : str   'cpu' or 'cuda'
    """

    def __init__(self, model_path: str,
                 label_path: str = None,
                 device: str = "cpu"):
        self.device = torch.device(device)

        # Load model
        self.model = SoilImageCNN()

        # ✅ FIX: try/except is now properly indented inside __init__
        try:
            print("🔄 Loading model from:", model_path)
            state = torch.load(model_path, map_location=self.device)
            self.model.load_state_dict(state, strict=False)
            self.model.eval()
            self.model.to(self.device)
            print("✅ Model loaded successfully")

        except Exception as e:
            print("❌ MODEL LOAD ERROR:", e)

        # ✅ FIX: label loading is now properly indented inside __init__
        if label_path:
            with open(label_path) as f:
                self.label_config = json.load(f)
        else:
            self.label_config = None

    @torch.no_grad()
    def analyze(self, image) -> dict:
        """
        Analyze a soil/crop image.

        Parameters
        ----------
        image : PIL.Image, numpy.ndarray, or file path (str)

        Returns
        -------
        dict with keys:
          predictions  – {soil_type, moisture, vegetation, crop_condition, disease}
          confidences  – confidence scores per task
          explanation  – human-readable string
          html         – styled HTML for Gradio display
        """
        # ── Preprocess ───────────────────────────────
        if image is None:
            return self._empty_result()

        if isinstance(image, str):
            pil_img = Image.open(image).convert("RGB")
        elif isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image.astype(np.uint8)).convert("RGB")
        elif isinstance(image, Image.Image):
            pil_img = image.convert("RGB")
        else:
            pil_img = Image.fromarray(image).convert("RGB")

        tensor = INFERENCE_TRANSFORMS(pil_img).unsqueeze(0).to(self.device)

        # ── Inference ────────────────────────────────
        outputs = self.model(tensor)

        # ── Decode predictions + confidences ─────────
        label_maps = {
            "soil_type":      SOIL_TYPES,
            "moisture":       MOISTURE_LABELS,
            "vegetation":     VEGETATION_LABELS,
            "crop_condition": CROP_CONDITION_LABELS,
            "disease":        DISEASE_LABELS,
        }

        predictions  = {}
        confidences  = {}
        all_probs    = {}

        for task, logits in outputs.items():
            probs    = torch.softmax(logits[0], dim=0).cpu().numpy()
            best_idx = int(probs.argmax())
            labels   = label_maps[task]
            predictions[task] = labels[best_idx]
            confidences[task] = float(probs[best_idx])
            all_probs[task]   = {labels[i]: float(probs[i])
                                 for i in range(len(labels))}

        # ── Generate explanation ──────────────────────
        explanation = generate_explanation(predictions)
        html        = generate_html_output(predictions, confidences, explanation)

        return {
            "predictions":  predictions,
            "confidences":  confidences,
            "all_probs":    all_probs,
            "explanation":  explanation,
            "html":         html,
        }

    def _empty_result(self) -> dict:
        return {
            "predictions":  {},
            "confidences":  {},
            "all_probs":    {},
            "explanation":  "No image provided. Please upload a soil or crop image.",
            "html":         "<p>📸 No image uploaded.</p>",
        }

    def get_image_tensor_for_multimodal(self, image) -> torch.Tensor:
        """
        Returns a (3, 224, 224) tensor suitable for passing into
        your existing SoilHealthModel's image branch.

        Use this in your inference pipeline to replace the dummy_img.
        """
        if image is None:
            return torch.zeros(3, 224, 224)

        if isinstance(image, np.ndarray):
            pil_img = Image.fromarray(image.astype(np.uint8)).convert("RGB")
        elif isinstance(image, Image.Image):
            pil_img = image.convert("RGB")
        else:
            pil_img = Image.open(image).convert("RGB")

        return INFERENCE_TRANSFORMS(pil_img)
#         return INFERENCE_TRANSFORMS(pil_img)