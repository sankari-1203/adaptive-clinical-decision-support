import React from "react";

export default function DecisionCard({ metrics, notice }) {
  if (!metrics) return null;

  const isRisk = metrics.final_prediction === 1;
  const isHighReliability = metrics.reliability === "HIGH";
  const isMedReliability = metrics.reliability === "MEDIUM";

  let cardTheme = "decision-high-risk";
  if (!isRisk && isHighReliability) cardTheme = "decision-low-risk";
  else if (isMedReliability) cardTheme = "decision-med-risk";
  else if (!isHighReliability && !isMedReliability) cardTheme = "decision-uncertain";

  return (
    <div className={`card decision-card ${cardTheme}`}>
      <div className="decision-header">
        <span className="badge-decision-risk">{metrics.risk_category}</span>
        <h2 className="decision-title">{metrics.decision_title}</h2>
        <p className="decision-subtitle">{metrics.decision_subtitle}</p>
      </div>

      <div className="recommendation-box">
        <span className="recommendation-heading">ADAPTIVE CLINICAL RECOMMENDATION</span>
        <p className="recommendation-text">{metrics.clinical_recommendation}</p>
      </div>

      <div className="regulatory-disclaimer-box">
        <svg
          className="disclaimer-icon"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          strokeWidth="2"
        >
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="8" x2="12" y2="12" />
          <line x1="12" y1="16" x2="12.01" y2="16" />
        </svg>
        <span>{notice || "For clinical decision support only. This prediction does not replace professional medical evaluation."}</span>
      </div>
    </div>
  );
}
