"""
Uncertainty and Entropy Tests
Verifies:
- Vote entropy calculation and safe handling of zero proportions
- Exact 0.81 value for 3-1 split
- Uncertainty quantification with alpha and beta
- Reliability level classification (HIGH, MEDIUM, LOW)
"""

import numpy as np
from app.uncertainty import compute_vote_entropy, quantify_uncertainty

def test_vote_entropy_values():
    # 4-0 unanimous vote (p_0 = 0, p_1 = 1) -> H = 0.0
    h_unanimous = compute_vote_entropy(np.array([1, 1, 1, 1]))
    assert abs(h_unanimous - 0.0) < 1e-5

    h_unanimous_zero = compute_vote_entropy(np.array([0, 0, 0, 0]))
    assert abs(h_unanimous_zero - 0.0) < 1e-5

    # 3-1 split (p_0 = 0.25, p_1 = 0.75) -> H = -0.25*log2(0.25) - 0.75*log2(0.75) = 0.811278
    h_split_3_1 = compute_vote_entropy(np.array([1, 1, 1, 0]))
    assert round(h_split_3_1, 2) == 0.81

    # 2-2 split (p_0 = 0.5, p_1 = 0.5) -> H = 1.0
    h_split_2_2 = compute_vote_entropy(np.array([1, 1, 0, 0]))
    assert abs(h_split_2_2 - 1.0) < 1e-5

def test_uncertainty_quantification_reliability_tiers():
    # High confidence (0.90) and unanimous (entropy=0.0)
    # Uncertainty = 0.6 * (1 - 0.90) + 0.4 * 0.0 = 0.06 -> HIGH
    u_high = quantify_uncertainty(
        np.array([1, 1, 1, 1]),
        np.array([0.9, 0.92, 0.88, 0.91]),
        weighted_confidence=0.90
    )
    assert u_high["reliability"] == "HIGH"
    assert u_high["uncertainty_score"] < 0.30

    # Moderate confidence with 3-1 split
    # If weighted_confidence = 0.65, H = 0.811 -> U = 0.6*(0.35) + 0.4*(0.811) = 0.21 + 0.324 = 0.534 -> MEDIUM
    u_med = quantify_uncertainty(
        np.array([1, 1, 1, 0]),
        np.array([0.7, 0.68, 0.62, 0.40]),
        weighted_confidence=0.65
    )
    assert u_med["reliability"] == "MEDIUM"

    # Low confidence with 2-2 split
    # If weighted_confidence = 0.52, H = 1.0 -> U = 0.6*(0.48) + 0.4*(1.0) = 0.288 + 0.4 = 0.688 -> LOW
    u_low = quantify_uncertainty(
        np.array([1, 1, 0, 0]),
        np.array([0.55, 0.53, 0.48, 0.46]),
        weighted_confidence=0.52
    )
    assert u_low["reliability"] == "LOW"
