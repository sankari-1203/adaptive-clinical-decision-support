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

    # 3. Standard Adaptive Support Statement (per Section 8 & Section 16 specification)
    if uncertainty_score < RELIABILITY_HIGH_THRESHOLD and disagreement_score <= DISAGREEMENT_LOW_THRESHOLD:
        if final_prediction == 1:
            clinical_recommendation = (
                f"HIGH CONFIDENCE — elevated predicted risk. Further clinical assessment is recommended."
            )
        else:
            clinical_recommendation = (
                f"HIGHER RELIABILITY — models consistently indicate lower predicted risk; "
                f"clinical context should still be considered."
            )
    elif uncertainty_score < RELIABILITY_MEDIUM_THRESHOLD:
        if final_prediction == 1:
            clinical_recommendation = (
                f"MODERATE/LOW CONFIDENCE — predicted risk with model disagreement. "
                f"Further clinical assessment is recommended."
            )
        else:
            clinical_recommendation = (
                f"MODERATE/LOW CONFIDENCE — lower predicted risk with model disagreement or uncertainty. "
                f"Further clinical review is recommended."
            )
    else:
        clinical_recommendation = (
            f"UNCERTAIN PREDICTION — model outputs are not sufficiently consistent. "
            f"Review patient information and consider further assessment."
        )

    return {
        "risk_category": risk_category,
        "decision_title": decision_title,
        "decision_subtitle": decision_subtitle,
        "clinical_recommendation": clinical_recommendation,
    }
