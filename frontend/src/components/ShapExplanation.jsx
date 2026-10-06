import React from "react";

export default function ShapExplanation({ shapData }) {
  if (!shapData || !shapData.feature_attributions) return null;

  const maxAttribution = Math.max(
    ...shapData.feature_attributions.map((f) => f.absolute_shap),
    0.001
  );

  return (
    <div className="card shap-card">
      <div className="section-header">
        <span className="badge-category">EXPLAINABLE AI (XAI)</span>
        <h2>SHAP Biomarker Attributions</h2>
      </div>

      <div className="shap-summary-callout">
        <strong>Biomarker Impact Analysis: </strong>
        <span>{shapData.shap_summary}</span>
      </div>

      <div className="shap-chart-container">
        <div className="shap-legend">
          <div className="legend-item">
            <span className="legend-color-box color-risk"></span>
            <span>Risk-Increasing Factor (Positive SHAP)</span>
          </div>
          <div className="legend-item">
            <span className="legend-color-box color-protective"></span>
            <span>Protective Factor (Negative SHAP)</span>
          </div>
        </div>

        <div className="shap-bars-list">
          {shapData.feature_attributions.map((item, idx) => {
            const isRisk = item.direction === "Risk-Increasing";
            const barWidth = Math.min((item.absolute_shap / maxAttribution) * 100, 100);

            return (
              <div key={idx} className="shap-bar-row">
                <div className="shap-feature-meta">
                  <span className="shap-feature-name">{item.feature}</span>
                  <span className="shap-patient-val">Value: {item.patient_value}</span>
                </div>

                <div className="shap-bar-track">
                  <div
                    className={`shap-bar-fill ${isRisk ? "shap-risk" : "shap-protective"}`}
                    style={{ width: `${barWidth}%` }}
                  ></div>
                </div>

                <div className="shap-val-col">
                  <span className={`shap-val-badge ${isRisk ? "text-risk" : "text-protective"}`}>
                    {item.shap_value > 0 ? `+${item.shap_value.toFixed(3)}` : item.shap_value.toFixed(3)}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      <p className="shap-disclaimer-text">
        <em>Notice: {shapData.disclaimer}</em>
      </p>
    </div>
  );
}
