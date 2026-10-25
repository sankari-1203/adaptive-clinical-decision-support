"""
Decision Engine Module
Converts ensemble risk, model agreement/disagreement, confidence, entropy,
and uncertainty into clinical decision support statements.
Adheres strictly to the wording specified in Section 8 & 16 of the project specification.
"""

from typing import Dict, Any
from app.config import (
    RISK_HIGH_THRESHOLD,
    RISK_MODERATE_THRESHOLD,
    RELIABILITY_HIGH_THRESHOLD,
    RELIABILITY_MEDIUM_THRESHOLD,
    DISAGREEMENT_LOW_THRESHOLD,
)

def synthesize_clinical_decision(
    disease_name: str,
    final_prediction: int,
    risk_probability: float,
    weighted_confidence: float,
    agreement_score: float,
    disagreement_score: float,
    uncertainty_score: float,
    reliability: str,
) -> Dict[str, str]:
    """
    Synthesizes the adaptive clinical decision and support wording.
    All outputs are clinical decision support guidance, not automated diagnoses.
    """
    d_upper = disease_name.upper()
    d_lower = disease_name.lower()

    # 1. Risk Category
    if risk_probability >= RISK_HIGH_THRESHOLD:
        risk_category = f"HIGH {d_upper} RISK"
    elif risk_probability >= RISK_MODERATE_THRESHOLD:
        risk_category = f"MODERATE {d_upper} RISK"
    else:
        risk_category = f"LOW {d_upper} RISK"

    # 2. Adaptive Clinical Decision Badge & Subtitle
    if reliability == "HIGH":
        if final_prediction == 1:
            decision_title = f"HIGH CONFIDENCE – {d_upper} RISK DETECTED"
            decision_subtitle = (
                "High model agreement. Clinical evaluation recommended based on patient context."
            )
        else:
            decision_title = f"HIGH CONFIDENCE – LOW {d_upper} RISK"
            decision_subtitle = (
                "High model agreement. Routine preventive care recommended."
            )
    elif reliability == "MEDIUM":
        if final_prediction == 1:
            decision_title = f"MODERATE CONFIDENCE – {d_upper} RISK"
            decision_subtitle = (
                "Predicted with model disagreement. Further clinical assessment recommended."
            )
        else:
            decision_title = f"MODERATE CONFIDENCE – LOW {d_upper} RISK"
            decision_subtitle = (
                "Low risk predicted with moderate uncertainty/disagreement. Review recommended."
            )
    else:  # LOW reliability / High uncertainty
        decision_title = "LOW CONFIDENCE – HIGH UNCERTAINTY"
        decision_subtitle = (
            f"Significant model disagreement on {d_lower} risk. "
            "Do not rely on automated prediction alone. Confirmatory clinical assessment required."
        )

    # 3. Final Adaptive Clinical Recommendation (strictly follows training notebook & clinical logic)
    if final_prediction == 1:
        if reliability == "HIGH":
            if "cardio" in d_lower:
                clinical_recommendation = (
                    "The ensemble predicts elevated cardiovascular risk with high reliability. "
                    "Clinical evaluation should consider the patient's symptoms, risk factors and "
                    "other relevant clinical information."
                )
            else:
                clinical_recommendation = (
                    "The ensemble predicts elevated diabetes risk with high reliability. "
                    "Clinical evaluation should consider the patient's symptoms, risk factors, "
                    "laboratory findings, and other relevant clinical information."
                )
        elif reliability == "MEDIUM":
            clinical_recommendation = (
                f"The ensemble predicts {d_lower} risk, but "
                "moderate uncertainty or model disagreement is present. "
                "Additional clinical information and professional assessment are recommended."
            )
        else:
            clinical_recommendation = (
                f"The {d_lower} risk prediction has high uncertainty. "
                "Do not rely on the automated prediction alone. "
                "Further clinical assessment is recommended."
            )
    else:
        if reliability == "HIGH":
            clinical_recommendation = (
                f"The ensemble predicts low {d_lower} risk "
                "with high reliability. Continue appropriate "
                "preventive care and routine monitoring based on "
                "patient context."
            )
        elif reliability == "MEDIUM":
            clinical_recommendation = (
                f"The ensemble predicts low {d_lower} risk, "
                "but model uncertainty or disagreement is present. "
                "Additional clinical review is recommended."
            )
        else:
            clinical_recommendation = (
                f"The prediction indicates low {d_lower} risk "
                "but has high uncertainty. The result should be "
                "interpreted cautiously and should not replace "
                "clinical assessment."
            )

    return {
        "risk_category": risk_category,
        "decision_title": decision_title,
        "decision_subtitle": decision_subtitle,
        "clinical_recommendation": clinical_recommendation,
    }
