"""
Ensemble Module
Calculates F1-weighted ensemble probability, individual and weighted confidence,
and model agreement/disagreement according to project specification.
"""

from typing import Dict, Any, List
import numpy as np
from app.config import MODEL_NAMES

def compute_individual_confidences(predictions: np.ndarray, probabilities: np.ndarray) -> np.ndarray:
    """
    Computes confidence of each model in its predicted class.
    C_i = max(P_i, 1 - P_i)
    """
    return np.maximum(probabilities, 1.0 - probabilities)

def calculate_ensemble_metrics(
    predictions: np.ndarray,
    probabilities: np.ndarray,
    weights: np.ndarray,
    disease_name: str = "Diabetes"
) -> Dict[str, Any]:
    """
    Calculates weighted ensemble metrics:
    - Weighted risk probability: sum(w_i * P_i)
    - Weighted confidence: sum(w_i * C_i)
    - Majority class prediction
    - Agreement and Disagreement scores
    """
    predictions = np.asarray(predictions, dtype=int)
    probabilities = np.asarray(probabilities, dtype=float)
    weights = np.asarray(weights, dtype=float)

    # Individual confidences: C_i = max(P_i, 1 - P_i)
    confidences = compute_individual_confidences(predictions, probabilities)

    # Weighted ensemble probability: P_ensemble = sum(w_i * P_i)
    ensemble_prob = float(np.sum(weights * probabilities))

    # Weighted confidence: C_weighted = sum(w_i * C_i)
    weighted_confidence = float(np.sum(weights * confidences))

    # Final prediction: Weighted average vote rounded
    weighted_vote_avg = float(np.average(predictions, weights=weights))
    final_prediction = int(np.round(weighted_vote_avg))

    # Agreement and Disagreement:
    # Agreement = (number of models supporting majority class / 4) * 100
    # Majority class can be determined by the most frequent vote among the 4 models
    counts = np.bincount(predictions, minlength=2)
    majority_count = int(np.max(counts))
    agreement_pct = float((majority_count / 4.0) * 100.0)
    disagreement_pct = float(100.0 - agreement_pct)

    # Per-model breakdown list
    model_breakdown = []
    for i, name in enumerate(MODEL_NAMES):
        model_breakdown.append({
            "model": name,
            "prediction_label": f"{disease_name}" if predictions[i] == 1 else f"No {disease_name}",
            "prediction_binary": int(predictions[i]),
            "risk_probability": float(probabilities[i]),
            "risk_probability_pct": f"{probabilities[i] * 100.0:.1f}%",
            "confidence": float(confidences[i]),
            "confidence_pct": f"{confidences[i] * 100.0:.1f}%",
            "weight": float(weights[i]),
            "weight_pct": f"{weights[i] * 100.0:.1f}%",
        })

    return {
        "final_prediction": final_prediction,
        "final_prediction_label": f"{disease_name}" if final_prediction == 1 else f"No {disease_name}",
        "risk_probability": ensemble_prob,
        "risk_probability_pct": f"{ensemble_prob * 100.0:.1f}%",
        "weighted_confidence": weighted_confidence,
        "weighted_confidence_pct": f"{weighted_confidence * 100.0:.1f}%",
        "agreement_score": agreement_pct / 100.0,
        "agreement_score_pct": f"{agreement_pct:.0f}%",
        "disagreement_score": disagreement_pct / 100.0,
        "disagreement_score_pct": f"{disagreement_pct:.0f}%",
        "model_results": model_breakdown,
        "confidences": confidences,
    }
