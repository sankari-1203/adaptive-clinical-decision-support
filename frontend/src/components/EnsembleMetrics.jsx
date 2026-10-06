import React from "react";

export default function EnsembleMetrics({ metrics }) {
  if (!metrics) return null;

  const reliability = metrics.reliability;
  let reliabilityBadgeClass = "badge-high";
  if (reliability === "MEDIUM") reliabilityBadgeClass = "badge-medium";
  if (reliability === "LOW") reliabilityBadgeClass = "badge-low";

  return (
    <div className="card ensemble-metrics-card">
      <div className="section-header">
        <div className="header-title-row">
          <span className="badge-category">MULTI-MODEL AGGREGATION</span>
          <span className={`badge-reliability ${reliabilityBadgeClass}`}>
            RELIABILITY: {reliability}
          </span>
        </div>
        <h2>Adaptive Ensemble & Reliability Quantification</h2>
      </div>

      <div className="ensemble-grid">
        <div className="ensemble-tile highlight-tile">
          <span className="tile-title">Ensemble Risk Probability</span>
          <span className="tile-number">{metrics.risk_probability_pct}</span>
          <span className="tile-subtitle">
            Weighted by Model F1-Scores (P_ensemble = Σ w_i * P_i)
          </span>
        </div>

        <div className="ensemble-tile">
          <span className="tile-title">Model Agreement</span>
          <span className="tile-number">{metrics.agreement_score_pct}</span>
          <span className="tile-subtitle">Proportion supporting majority vote</span>
        </div>

        <div className="ensemble-tile">
          <span className="tile-title">Model Disagreement</span>
          <span className="tile-number">{metrics.disagreement_score_pct}</span>
          <span className="tile-subtitle">100% - Agreement Score</span>
        </div>

        <div className="ensemble-tile">
          <span className="tile-title">Weighted Confidence</span>
          <span className="tile-number">{metrics.weighted_confidence_pct}</span>
          <span className="tile-subtitle">Confidence = Σ w_i * max(P_i, 1 - P_i)</span>
        </div>

        <div className="ensemble-tile">
          <span className="tile-title">Vote Entropy (H)</span>
          <span className="tile-number">{metrics.vote_entropy_str}</span>
          <span className="tile-subtitle">H = -Σ p_k * log₂(p_k)</span>
        </div>

        <div className="ensemble-tile">
          <span className="tile-title">Uncertainty Score</span>
          <span className="tile-number">{metrics.uncertainty_score_str}</span>
          <span className="tile-subtitle">0.6*(1 - Conf) + 0.4*Entropy</span>
        </div>
      </div>
    </div>
  );
}
