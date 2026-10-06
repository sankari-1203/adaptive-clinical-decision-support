import React from "react";

export default function DiseaseSelector({ selectedDisease, onSelectDisease, loading }) {
  return (
    <div className="card disease-selector-card">
      <div className="section-header">
        <span className="badge-category">SELECT CLINICAL PROTOCOL</span>
        <h2>Active Disease Pipeline</h2>
      </div>
      <div className="selector-control">
        <label htmlFor="disease-dropdown" className="selector-label">
          Disease Target:
        </label>
        <select
          id="disease-dropdown"
          className="form-select disease-dropdown"
          value={selectedDisease}
          onChange={(e) => onSelectDisease(e.target.value)}
          disabled={loading}
        >
          <option value="diabetes">Diabetes Mellitus Pipeline (8 Biomarkers)</option>
          <option value="cardiovascular">Cardiovascular Disease Pipeline (11 Clinical Indicators)</option>
        </select>
      </div>
      <p className="pipeline-note">
        {selectedDisease === "diabetes"
          ? "Loads saved Diabetes models (LR, SVM, RF, XGBoost) and categorical encoders. Independent feature space."
          : "Loads saved Cardiovascular models (LR, SVM, RF, XGBoost) and standard scaler. Independent feature space."}
      </p>
    </div>
  );
}
