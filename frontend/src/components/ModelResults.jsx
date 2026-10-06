import React from "react";

export default function ModelResults({ modelResults }) {
  if (!modelResults || modelResults.length === 0) return null;

  return (
    <div className="card model-results-card">
      <div className="section-header">
        <span className="badge-category">INDEPENDENT INFERENCE</span>
        <h2>Individual Model Predictions</h2>
      </div>

      <div className="models-grid">
        {modelResults.map((item, idx) => {
          const isPositive = item.prediction_binary === 1;
          const probPct = (item.risk_probability * 100).toFixed(1);

          return (
            <div
              key={idx}
              className={`model-card ${isPositive ? "status-positive" : "status-negative"}`}
            >
              <div className="model-header">
                <span className="model-name">{item.model}</span>
                <span className={`model-tag ${isPositive ? "tag-risk" : "tag-safe"}`}>
                  {item.prediction_label}
                </span>
              </div>

              <div className="model-metrics-row">
                <div className="metric-box">
                  <span className="metric-label">Risk Probability</span>
                  <span className="metric-value">{probPct}%</span>
                </div>
                <div className="metric-box">
                  <span className="metric-label">Confidence</span>
                  <span className="metric-value">{item.confidence_pct}</span>
                </div>
                <div className="metric-box">
                  <span className="metric-label">F1 Weight</span>
                  <span className="metric-value">{item.weight_pct}</span>
                </div>
              </div>

              <div className="progress-bar-container">
                <div
                  className={`progress-fill ${isPositive ? "fill-risk" : "fill-safe"}`}
                  style={{ width: `${probPct}%` }}
                ></div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
