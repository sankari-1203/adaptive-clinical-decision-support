import React from "react";

export default function PatientForm({
  disease,
  formData,
  onChangeField,
  onSubmit,
  loading,
  onLoadPreset,
}) {
  const isDiabetes = disease === "diabetes";

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit();
  };

  return (
    <div className="card patient-form-card">
      <div className="section-header">
        <div className="header-title-row">
          <span className="badge-category">STRUCTURED CLINICAL INPUT</span>
          <div className="preset-buttons">
            <span className="preset-label">Demonstration Cases:</span>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => onLoadPreset("normal")}
              disabled={loading}
            >
              Normal Case
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => onLoadPreset("elevated")}
              disabled={loading}
            >
              Elevated Risk Case
            </button>
            <button
              type="button"
              className="btn btn-secondary btn-sm"
              onClick={() => onLoadPreset("borderline")}
              disabled={loading}
            >
              Borderline Case
            </button>
          </div>
        </div>
        <h2>Patient Clinical Information</h2>
      </div>

      <form onSubmit={handleSubmit} className="clinical-grid-form">
        {isDiabetes ? (
          <>
            <div className="form-group">
              <label htmlFor="gender">Gender</label>
              <select
                id="gender"
                className="form-select"
                value={formData.gender || "Female"}
                onChange={(e) => onChangeField("gender", e.target.value)}
                disabled={loading}
                required
              >
                <option value="Female">Female</option>
                <option value="Male">Male</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="age">Age (years)</label>
              <input
                id="age"
                type="number"
                step="1"
                min="1"
                max="120"
                className="form-input"
                value={formData.age ?? 45}
                onChange={(e) => onChangeField("age", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="hypertension">Hypertension</label>
              <select
                id="hypertension"
                className="form-select"
                value={formData.hypertension ?? 0}
                onChange={(e) => onChangeField("hypertension", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="heart_disease">Heart Disease</label>
              <select
                id="heart_disease"
                className="form-select"
                value={formData.heart_disease ?? 0}
                onChange={(e) => onChangeField("heart_disease", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="smoking_history">Smoking History</label>
              <select
                id="smoking_history"
                className="form-select"
                value={formData.smoking_history || "never"}
                onChange={(e) => onChangeField("smoking_history", e.target.value)}
                disabled={loading}
                required
              >
                <option value="never">Never</option>
                <option value="No Info">No Info</option>
                <option value="current">Current</option>
                <option value="former">Former</option>
                <option value="ever">Ever</option>
                <option value="not current">Not Current</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="bmi">BMI (kg/m²)</label>
              <input
                id="bmi"
                type="number"
                step="0.1"
                min="10"
                max="90"
                className="form-input"
                value={formData.bmi ?? 25.4}
                onChange={(e) => onChangeField("bmi", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="HbA1c_level">HbA1c Level (%)</label>
              <input
                id="HbA1c_level"
                type="number"
                step="0.1"
                min="3.0"
                max="16.0"
                className="form-input"
                value={formData.HbA1c_level ?? 5.8}
                onChange={(e) => onChangeField("HbA1c_level", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="blood_glucose_level">Blood Glucose (mg/dL)</label>
              <input
                id="blood_glucose_level"
                type="number"
                step="1"
                min="40"
                max="400"
                className="form-input"
                value={formData.blood_glucose_level ?? 110}
                onChange={(e) => onChangeField("blood_glucose_level", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>
          </>
        ) : (
          <>
            <div className="form-group">
              <label htmlFor="age_years">Age (years)</label>
              <input
                id="age_years"
                type="number"
                step="0.1"
                min="18"
                max="100"
                className="form-input"
                value={formData.age_years ?? 50.4}
                onChange={(e) => onChangeField("age_years", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="cardio_gender">Gender</label>
              <select
                id="cardio_gender"
                className="form-select"
                value={formData.gender ?? 1}
                onChange={(e) => onChangeField("gender", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={1}>Female (1)</option>
                <option value={2}>Male (2)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="height">Height (cm)</label>
              <input
                id="height"
                type="number"
                step="0.5"
                min="100"
                max="250"
                className="form-input"
                value={formData.height ?? 168.0}
                onChange={(e) => onChangeField("height", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="weight">Weight (kg)</label>
              <input
                id="weight"
                type="number"
                step="0.5"
                min="30"
                max="250"
                className="form-input"
                value={formData.weight ?? 62.0}
                onChange={(e) => onChangeField("weight", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="ap_hi">Systolic BP (ap_hi mmHg)</label>
              <input
                id="ap_hi"
                type="number"
                step="1"
                min="60"
                max="240"
                className="form-input"
                value={formData.ap_hi ?? 110.0}
                onChange={(e) => onChangeField("ap_hi", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="ap_lo">Diastolic BP (ap_lo mmHg)</label>
              <input
                id="ap_lo"
                type="number"
                step="1"
                min="40"
                max="160"
                className="form-input"
                value={formData.ap_lo ?? 80.0}
                onChange={(e) => onChangeField("ap_lo", parseFloat(e.target.value))}
                disabled={loading}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="cholesterol">Cholesterol Level</label>
              <select
                id="cholesterol"
                className="form-select"
                value={formData.cholesterol ?? 1}
                onChange={(e) => onChangeField("cholesterol", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={1}>1: Normal</option>
                <option value={2}>2: Above Normal</option>
                <option value={3}>3: Well Above Normal</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="gluc">Glucose Level</label>
              <select
                id="gluc"
                className="form-select"
                value={formData.gluc ?? 1}
                onChange={(e) => onChangeField("gluc", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={1}>1: Normal</option>
                <option value={2}>2: Above Normal</option>
                <option value={3}>3: Well Above Normal</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="smoke">Smoker</label>
              <select
                id="smoke"
                className="form-select"
                value={formData.smoke ?? 0}
                onChange={(e) => onChangeField("smoke", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="alco">Alcohol Intake</label>
              <select
                id="alco"
                className="form-select"
                value={formData.alco ?? 0}
                onChange={(e) => onChangeField("alco", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={0}>No (0)</option>
                <option value={1}>Yes (1)</option>
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="active">Physical Activity</label>
              <select
                id="active"
                className="form-select"
                value={formData.active ?? 1}
                onChange={(e) => onChangeField("active", parseInt(e.target.value, 10))}
                disabled={loading}
                required
              >
                <option value={1}>Active (1)</option>
                <option value={0}>Sedentary (0)</option>
              </select>
            </div>
          </>
        )}

        <div className="form-action-row">
          <button
            type="submit"
            className="btn btn-primary btn-block predict-btn"
            disabled={loading}
          >
            {loading ? (
              <span className="spinner-wrap">
                <span className="spinner"></span> Processing Multi-Model Inference...
              </span>
            ) : isDiabetes ? (
              "PREDICT DIABETES RISK"
            ) : (
              "PREDICT CARDIOVASCULAR RISK"
            )}
          </button>
        </div>
      </form>
    </div>
  );
}
