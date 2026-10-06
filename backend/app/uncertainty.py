"""
Uncertainty Quantification Module
Calculates vote entropy, probability variance, adaptive uncertainty score, and reliability tiering.
"""

from typing import Dict, Any
import numpy as np
from app.config import (
    UNCERTAINTY_ALPHA,
    UNCERTAINTY_BETA,
    RELIABILITY_HIGH_THRESHOLD,
    RELIABILITY_MEDIUM_THRESHOLD,
)

def compute_vote_entropy(predictions: np.ndarray) -> float:
    """
    Computes binary vote entropy using log base 2:
    H = - sum(p_k * log2(p_k))
    Handles p_k = 0 safely.
    For 4 models:
    - 4-0 split: H = 0.00
    - 3-1 split: H = 0.81
    - 2-2 split: H = 1.00
    """
    predictions = np.asarray(predictions, dtype=int)
    counts = np.bincount(predictions, minlength=2)
    proportions = counts / float(len(predictions))

    entropy_val = 0.0
    for p in proportions:
        if p > 0.0:
            entropy_val -= p * np.log2(p)

    return float(entropy_val)

def quantify_uncertainty(
    predictions: np.ndarray,
    probabilities: np.ndarray,
    weighted_confidence: float,
    alpha: float = UNCERTAINTY_ALPHA,
    beta: float = UNCERTAINTY_BETA,
) -> Dict[str, Any]:
    """
    Quantifies uncertainty using:
    - Vote entropy H
    - Normalized entropy (in [0, 1])
    - Probability variance across the 4 models
    - Adaptive uncertainty score = alpha * (1 - weighted_confidence) + beta * normalized_entropy
    - Reliability tier: HIGH, MEDIUM, LOW
    """
    # 1. Vote entropy
    vote_entropy = compute_vote_entropy(predictions)
    max_entropy = 1.0  # log2(2) for binary
    normalized_entropy = float(np.clip(vote_entropy / max_entropy, 0.0, 1.0))

    # 2. Probability variance
    prob_variance = float(np.var(probabilities))

    # 3. Adaptive uncertainty score
    uncertainty_score = float(alpha * (1.0 - weighted_confidence) + beta * normalized_entropy)

    # 4. Reliability Level
    if uncertainty_score < RELIABILITY_HIGH_THRESHOLD:
        reliability = "HIGH"
    elif uncertainty_score < RELIABILITY_MEDIUM_THRESHOLD:
        reliability = "MEDIUM"
    else:
        reliability = "LOW"

    return {
        "vote_entropy": vote_entropy,
        "vote_entropy_str": f"{vote_entropy:.2f}",
        "normalized_entropy": normalized_entropy,
        "probability_variance": prob_variance,
        "probability_variance_str": f"{prob_variance:.4f}",
        "uncertainty_score": uncertainty_score,
        "uncertainty_score_str": f"{uncertainty_score:.2f}",
        "reliability": reliability,
    }
