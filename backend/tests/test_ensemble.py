"""
Ensemble Logic Tests
Validates mathematical correctness of:
- F1-derived weighted probability: P_ensemble = sum(w_i * P_i)
- Agreement: (majority supporting / 4) * 100
- Disagreement: 100 - Agreement
- Individual & Weighted Confidence: C_i = max(P_i, 1 - P_i), C_weighted = sum(w_i * C_i)
"""

import numpy as np
from app.ensemble import compute_individual_confidences, calculate_ensemble_metrics

def test_individual_confidences():
    preds = np.array([1, 1, 0, 1])
    probs = np.array([0.80, 0.65, 0.40, 0.90])
    conf = compute_individual_confidences(preds, probs)
    # max(0.8, 0.2) = 0.8; max(0.65, 0.35) = 0.65; max(0.4, 0.6) = 0.6; max(0.9, 0.1) = 0.9
    expected = np.array([0.80, 0.65, 0.60, 0.90])
    np.testing.assert_allclose(conf, expected)

def test_weighted_ensemble_metrics():
    preds = np.array([1, 1, 1, 0])
    probs = np.array([0.80, 0.70, 0.60, 0.30])
    weights = np.array([0.25, 0.25, 0.25, 0.25])

    res = calculate_ensemble_metrics(preds, probs, weights, disease_name="Diabetes")

    # Weighted probability = 0.25 * (0.8 + 0.7 + 0.6 + 0.3) = 0.60
    assert abs(res["risk_probability"] - 0.60) < 1e-5

    # Agreement: 3 models say 1, 1 says 0 -> (3/4)*100 = 75%
    assert res["agreement_score_pct"] == "75%"
    assert res["disagreement_score_pct"] == "25%"

    # Weighted confidence: confidences = [0.8, 0.7, 0.6, 0.7] -> avg = 0.70
    assert abs(res["weighted_confidence"] - 0.70) < 1e-5
