"""
=============================================================
 Decision Support Layer
 Rule-based, interpretable, domain-grounded recommendations

 WHY rule-based?
   - Deep learning black boxes are hard to trust for farmers
   - Rules are explainable, auditable, and easily updated
   - No training data needed for the recommendation layer
   - Rules encode real agronomic knowledge
=============================================================
"""

from dataclasses import dataclass, field
from typing import List, Optional
import json


# ─────────────────────────────────────────────────────────
# 1. Data container for model predictions + raw features
# ─────────────────────────────────────────────────────────
@dataclass
class SoilProfile:
    """Input features for the decision support layer."""
    # Raw tabular features
    N: float                    # kg/ha
    P: float                    # kg/ha
    K: float                    # kg/ha
    pH: float
    rainfall: float             # mm
    temperature: float          # °C
    humidity: float             # %
    organic_carbon: float       # %
    sand: float                 # %

    # Model predictions (filled by predict_full())
    shi: float = 0.0            # Soil Health Index [0, 1]
    soil_class: str = ""        # Poor / Moderate / Healthy


# ─────────────────────────────────────────────────────────
# 2. Crop Recommendation
# ─────────────────────────────────────────────────────────
# Crop suitability rules: each crop has min/max for key features
# Thresholds sourced from standard agronomic references (ICAR, FAO)
CROP_RULES = {
    "Rice": {
        "N": (60, 140), "P": (30, 145), "K": (30, 120),
        "pH": (5.0, 7.5), "rainfall": (150, 300),
        "temperature": (20, 35), "shi_min": 0.30,
    },
    "Maize": {
        "N": (50, 140), "P": (30, 100), "K": (30, 120),
        "pH": (5.5, 7.5), "rainfall": (50, 200),
        "temperature": (18, 35), "shi_min": 0.30,
    },
    "Wheat": {
        "N": (40, 120), "P": (25, 90), "K": (20, 100),
        "pH": (5.5, 7.5), "rainfall": (30, 150),
        "temperature": (10, 25), "shi_min": 0.30,
    },
    "Chickpea": {
        "N": (0, 60), "P": (40, 120), "K": (20, 100),
        "pH": (5.5, 7.5), "rainfall": (60, 150),
        "temperature": (15, 30), "shi_min": 0.25,
    },
    "Lentil": {
        "N": (0, 50), "P": (30, 100), "K": (20, 80),
        "pH": (5.5, 7.5), "rainfall": (25, 100),
        "temperature": (10, 25), "shi_min": 0.25,
    },
    "Cotton": {
        "N": (60, 140), "P": (20, 80), "K": (20, 100),
        "pH": (5.5, 8.0), "rainfall": (50, 150),
        "temperature": (20, 38), "shi_min": 0.30,
    },
    "Sugarcane": {
        "N": (80, 140), "P": (20, 80), "K": (40, 120),
        "pH": (5.5, 7.5), "rainfall": (100, 250),
        "temperature": (20, 38), "shi_min": 0.35,
    },
    "Soybean": {
        "N": (0, 70), "P": (30, 100), "K": (20, 100),
        "pH": (6.0, 7.5), "rainfall": (60, 180),
        "temperature": (18, 33), "shi_min": 0.30,
    },
    "Groundnut": {
        "N": (0, 60), "P": (30, 100), "K": (20, 100),
        "pH": (5.5, 7.5), "rainfall": (50, 150),
        "temperature": (20, 35), "shi_min": 0.25,
    },
    "Mango": {
        "N": (30, 100), "P": (20, 70), "K": (20, 90),
        "pH": (5.5, 7.5), "rainfall": (75, 200),
        "temperature": (24, 40), "shi_min": 0.35,
    },
    "Banana": {
        "N": (80, 140), "P": (30, 100), "K": (80, 145),
        "pH": (5.5, 7.0), "rainfall": (100, 300),
        "temperature": (20, 35), "shi_min": 0.35,
    },
    "Coffee": {
        "N": (40, 100), "P": (20, 70), "K": (30, 100),
        "pH": (5.0, 6.5), "rainfall": (150, 300),
        "temperature": (15, 28), "shi_min": 0.40,
    },
    "Jute": {
        "N": (60, 130), "P": (20, 80), "K": (20, 80),
        "pH": (6.0, 7.5), "rainfall": (150, 300),
        "temperature": (25, 37), "shi_min": 0.30,
    },
}


def recommend_crops(profile: SoilProfile, max_results: int = 3) -> List[dict]:
    """
    Score each crop against the soil profile.
    Returns top-N crops sorted by score (higher = better match).

    Scoring: each feature within range contributes 1 point.
    SHI below shi_min → crop is excluded entirely.
    """
    scores = []
    features = {
        "N": profile.N, "P": profile.P, "K": profile.K,
        "pH": profile.pH, "rainfall": profile.rainfall,
        "temperature": profile.temperature,
    }

    for crop, rules in CROP_RULES.items():
        # Hard gate: soil must be healthy enough for this crop
        if profile.shi < rules["shi_min"]:
            continue

        score = 0
        total = 0
        reasons = []

        for feat, rule_val in rules.items():
            if feat == "shi_min":
                continue
            lo, hi = rule_val
            val = features.get(feat, None)
            if val is None:
                continue
            total += 1
            if lo <= val <= hi:
                score += 1
            else:
                diff = min(abs(val - lo), abs(val - hi))
                reasons.append(f"{feat} slightly {'low' if val < lo else 'high'} ({val:.1f})")

        if total > 0:
            pct = score / total * 100
            scores.append({
                "crop": crop,
                "score_pct": round(pct, 1),
                "suitability": "High" if pct >= 80 else "Medium" if pct >= 60 else "Low",
                "issues": reasons[:2],  # top 2 limiting factors
            })

    scores.sort(key=lambda x: x["score_pct"], reverse=True)
    return scores[:max_results]


# ─────────────────────────────────────────────────────────
# 3. Fertilizer Suggestion
# ─────────────────────────────────────────────────────────
# Reference ranges (general guidelines; adjust for specific crops)
NUTRIENT_NORMS = {
    "N":  {"low": 30, "high": 100},   # kg/ha
    "P":  {"low": 25, "high": 100},   # kg/ha
    "K":  {"low": 25, "high": 100},   # kg/ha
}


def suggest_fertilizer(profile: SoilProfile) -> dict:
    """
    Detect N/P/K deficiencies or toxicities.
    Returns actionable fertilizer advice.

    WHY rule-based here?
    - Fertilizer recommendations need to be auditable
    - A wrong deep-learning recommendation could waste money or harm crops
    - Simple thresholds match what extension officers use in practice
    """
    recommendations = []
    status = {}

    for nutrient, norms in NUTRIENT_NORMS.items():
        val = getattr(profile, nutrient)
        lo, hi = norms["low"], norms["high"]

        if val < lo:
            deficit = lo - val
            status[nutrient] = "Deficient"
            if nutrient == "N":
                rec = (f"Nitrogen is LOW ({val:.0f} kg/ha). "
                       f"Apply ~{deficit:.0f} kg/ha Urea or DAP. "
                       "Consider split application (50% basal, 50% topdress).")
            elif nutrient == "P":
                rec = (f"Phosphorus is LOW ({val:.0f} kg/ha). "
                       f"Apply ~{deficit:.0f} kg/ha SSP or DAP. "
                       "Best applied at sowing for root development.")
            else:  # K
                rec = (f"Potassium is LOW ({val:.0f} kg/ha). "
                       f"Apply ~{deficit:.0f} kg/ha MOP (Muriate of Potash). "
                       "Critical for disease resistance and water use.")
            recommendations.append(rec)

        elif val > hi:
            status[nutrient] = "Excess"
            rec = (f"{nutrient} is HIGH ({val:.0f} kg/ha). "
                   "Avoid further fertilization for this nutrient. "
                   "Excess can cause toxicity or nutrient lockout.")
            recommendations.append(rec)
        else:
            status[nutrient] = "Optimal"

    # Organic carbon check
    if profile.organic_carbon < 5.0:
        recommendations.append(
            f"Organic carbon is LOW ({profile.organic_carbon:.1f}%). "
            "Add compost or vermicompost (2–5 tons/ha) to improve "
            "soil structure, water retention, and microbial activity."
        )

    # pH-based nutrient availability warnings
    if profile.pH < 5.5:
        recommendations.append(
            f"Soil pH is very acidic ({profile.pH:.1f}). "
            "Apply lime (calcium carbonate) to raise pH. "
            "Acidic soils lock up P and cause Al/Mn toxicity."
        )
    elif profile.pH > 8.0:
        recommendations.append(
            f"Soil pH is alkaline ({profile.pH:.1f}). "
            "Apply gypsum or sulfur to lower pH. "
            "Alkaline soils reduce Fe, Mn, Zn availability."
        )

    if not recommendations:
        recommendations.append(
            "Nutrient levels are within optimal range. "
            "Maintain with balanced NPK fertilization."
        )

    return {
        "nutrient_status": status,
        "recommendations": recommendations,
    }


# ─────────────────────────────────────────────────────────
# 4. Irrigation Recommendation
# ─────────────────────────────────────────────────────────
def recommend_irrigation(profile: SoilProfile) -> dict:
    """
    Estimate irrigation need from rainfall, humidity, temperature, and sand%.

    Logic:
    - High rainfall + high humidity = low irrigation need
    - Sandy soils drain faster → need more irrigation
    - High temperature = more evapotranspiration → more irrigation
    - Output: Low / Medium / High irrigation + frequency advice
    """
    score = 0  # Higher = more irrigation needed

    # Rainfall contribution
    if profile.rainfall < 50:
        score += 3
    elif profile.rainfall < 100:
        score += 2
    elif profile.rainfall < 200:
        score += 1
    # > 200 mm → score += 0

    # Humidity contribution
    if profile.humidity < 40:
        score += 2
    elif profile.humidity < 60:
        score += 1

    # Temperature / evapotranspiration
    if profile.temperature > 35:
        score += 2
    elif profile.temperature > 28:
        score += 1

    # Sandy soil drains fast
    if profile.sand > 70:
        score += 2
    elif profile.sand > 50:
        score += 1

    # Classify
    if score <= 2:
        level = "Low"
        advice = ("Rainfall and humidity are sufficient. "
                  "Monitor soil moisture; irrigate only if wilting is observed.")
        frequency = "Once every 10–14 days or as needed"
    elif score <= 5:
        level = "Medium"
        advice = ("Moderate irrigation required. "
                  "Use drip irrigation to minimise water loss. "
                  "Irrigate at dawn/dusk to reduce evaporation.")
        frequency = "Once every 5–7 days"
    else:
        level = "High"
        advice = ("High irrigation demand. "
                  "Sandy soil or high temperature is driving water loss. "
                  "Consider mulching to retain soil moisture. "
                  "Drip or micro-sprinkler irrigation recommended.")
        frequency = "Every 2–3 days; check soil at 5 cm depth"

    return {
        "irrigation_level": level,
        "advice": advice,
        "frequency": frequency,
        "contributing_factors": {
            "rainfall_mm": profile.rainfall,
            "humidity_pct": profile.humidity,
            "temperature_c": profile.temperature,
            "sand_pct": profile.sand,
        },
    }


# ─────────────────────────────────────────────────────────
# 5. Full Decision Support Output
# ─────────────────────────────────────────────────────────
def generate_full_report(profile: SoilProfile) -> dict:
    """
    Combines model predictions + all rule-based recommendations
    into a single structured output (JSON-serialisable).
    """
    crops      = recommend_crops(profile, max_results=3)
    fertilizer = suggest_fertilizer(profile)
    irrigation = recommend_irrigation(profile)

    report = {
        "soil_assessment": {
            "soil_health_index": round(profile.shi, 4),
            "soil_class": profile.soil_class,
            "interpretation": (
                "Soil is in poor condition. Immediate remediation needed."
                if profile.soil_class == "Poor" else
                "Soil is moderately healthy. Targeted improvements recommended."
                if profile.soil_class == "Moderate" else
                "Soil is healthy. Maintain current practices."
            ),
        },
        "crop_recommendations": crops,
        "fertilizer_advice": fertilizer,
        "irrigation_advice": irrigation,
        "raw_inputs": {
            "N": profile.N, "P": profile.P, "K": profile.K,
            "pH": profile.pH, "rainfall": profile.rainfall,
            "temperature": profile.temperature, "humidity": profile.humidity,
            "organic_carbon": profile.organic_carbon, "sand": profile.sand,
        },
    }
    return report


def print_report(report: dict):
    """Pretty-print the full recommendation report."""
    print("\n" + "=" * 60)
    print("🌱  SOIL HEALTH & CROP ADVISORY REPORT")
    print("=" * 60)

    sa = report["soil_assessment"]
    print(f"\n📊 SOIL HEALTH")
    print(f"   Index (SHI):  {sa['soil_health_index']:.4f}  (0=worst, 1=best)")
    print(f"   Class:        {sa['soil_class']}")
    print(f"   Assessment:   {sa['interpretation']}")

    print(f"\n🌾 CROP RECOMMENDATIONS")
    crops = report["crop_recommendations"]
    if crops:
        for i, c in enumerate(crops, 1):
            issues = ", ".join(c["issues"]) if c["issues"] else "All conditions met"
            print(f"   {i}. {c['crop']} — {c['suitability']} suitability ({c['score_pct']}%)")
            print(f"      Limiting factors: {issues}")
    else:
        print("   No suitable crops found for current soil conditions.")
        print("   Focus on soil remediation first.")

    print(f"\n🧪 FERTILIZER ADVICE")
    for nutrient, status in report["fertilizer_advice"]["nutrient_status"].items():
        print(f"   {nutrient}: {status}")
    print("   Recommendations:")
    for rec in report["fertilizer_advice"]["recommendations"]:
        print(f"   • {rec}")

    print(f"\n💧 IRRIGATION ADVICE")
    irr = report["irrigation_advice"]
    print(f"   Need Level: {irr['irrigation_level']}")
    print(f"   Frequency:  {irr['frequency']}")
    print(f"   Advice:     {irr['advice']}")

    print("\n" + "=" * 60)