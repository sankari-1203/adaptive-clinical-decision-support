import React, { useState } from "react";
import DiseaseSelector from "./components/DiseaseSelector";
import PatientForm from "./components/PatientForm";
import ModelResults from "./components/ModelResults";
import EnsembleMetrics from "./components/EnsembleMetrics";
import DecisionCard from "./components/DecisionCard";
import ShapExplanation from "./components/ShapExplanation";
import { predictDisease } from "./api/predictionApi";
import "./styles/app.css";

const DIABETES_DEFAULTS = {
  gender: "Female",
  age: 45,
  hypertension: 0,
  heart_disease: 0,
  smoking_history: "never",
  bmi: 25.4,
  HbA1c_level: 5.8,
  blood_glucose_level: 110,
};

const CARDIO_DEFAULTS = {
  age_years: 50.4,
  gender: 1,
  height: 168.0,
  weight: 62.0,
  ap_hi: 110.0,
  ap_lo: 80.0,
  cholesterol: 1,
  gluc: 1,
  smoke: 0,
  alco: 0,
  active: 1,
};

const PRESETS = {
  diabetes: {
    normal: {
      gender: "Female",
      age: 38,
      hypertension: 0,
      heart_disease: 0,
      smoking_history: "never",
      bmi: 22.1,
      HbA1c_level: 5.2,
      blood_glucose_level: 95,
    },
    elevated: {
      gender: "Male",
      age: 62,
      hypertension: 1,
      heart_disease: 1,
      smoking_history: "current",
      bmi: 34.2,
      HbA1c_level: 8.4,
      blood_glucose_level: 210,
    },
    borderline: {
      gender: "Female",
      age: 52,
      hypertension: 1,
      heart_disease: 0,
      smoking_history: "former",
      bmi: 28.5,
      HbA1c_level: 6.4,
      blood_glucose_level: 140,
    },
  },
  cardiovascular: {
    normal: {
      age_years: 50.4,
      gender: 1,
      height: 168.0,
      weight: 62.0,
      ap_hi: 110.0,
      ap_lo: 80.0,
      cholesterol: 1,
      gluc: 1,
      smoke: 0,
      alco: 0,
      active: 1,
    },
    elevated: {
      age_years: 64.0,
      gender: 2,
      height: 172.0,
      weight: 92.0,
      ap_hi: 165.0,
      ap_lo: 105.0,
      cholesterol: 3,
      gluc: 2,
      smoke: 1,
      alco: 1,
      active: 0,
    },
    borderline: {
      age_years: 54.0,
      gender: 1,
      height: 162.0,
      weight: 76.0,
      ap_hi: 132.0,
      ap_lo: 86.0,
      cholesterol: 2,
      gluc: 1,
      smoke: 0,
      alco: 0,
      active: 1,
    },
  },
};

export default function App() {
  const [selectedDisease, setSelectedDisease] = useState("diabetes");
  const [formData, setFormData] = useState(DIABETES_DEFAULTS);
  const [predictionResult, setPredictionResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState(null);

  const handleDiseaseChange = (disease) => {
    setSelectedDisease(disease);
    setPredictionResult(null);
    setErrorMsg(null);
    if (disease === "diabetes") {
      setFormData(DIABETES_DEFAULTS);
    } else {
      setFormData(CARDIO_DEFAULTS);
    }
  };

  const handleFieldChange = (field, value) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
  };

  const handleLoadPreset = (presetKey) => {
    const preset = PRESETS[selectedDisease]?.[presetKey];
    if (preset) {
      setFormData({ ...preset });
      setPredictionResult(null);
      setErrorMsg(null);
    }
  };

  const handleSubmit = async () => {
    setLoading(true);
    setErrorMsg(null);
    try {
      const data = await predictDisease(selectedDisease, formData);
      setPredictionResult(data);
    } catch (err) {
      console.error("Prediction failed:", err);
      const detail = err.response?.data?.detail || err.message || "An unexpected error occurred.";
      setErrorMsg(typeof detail === "string" ? detail : JSON.stringify(detail));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand-row">
          <svg className="brand-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
          </svg>
          <div>
            <h1>ADAPTIVE CLINICAL DECISION SUPPORT</h1>
            <p className="header-subtitle">
              Uncertainty-Aware Multi-Model Ensemble Learning & SHAP Explainability System
            </p>
          </div>
        </div>
      </header>

      <div className="regulatory-bar">
        <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2">
          <circle cx="12" cy="12" r="10" />
          <line x1="12" y1="16" x2="12" y2="12" />
          <line x1="12" y1="8" x2="12.01" y2="8" />
        </svg>
        <span>
          <strong>Clinical Notice:</strong> For clinical decision support only. This prediction does not replace
          professional medical evaluation.
        </span>
      </div>

      <DiseaseSelector
        selectedDisease={selectedDisease}
        onSelectDisease={handleDiseaseChange}
        loading={loading}
      />

      {errorMsg && (
        <div className="error-banner">
          <strong>Clinical Pipeline Error: </strong>
          <span>{errorMsg}</span>
        </div>
      )}

      <PatientForm
        disease={selectedDisease}
        formData={formData}
        onChangeField={handleFieldChange}
        onSubmit={handleSubmit}
        loading={loading}
        onLoadPreset={handleLoadPreset}
      />

      {predictionResult && (
        <>
          <DecisionCard
            metrics={predictionResult.ensemble_metrics}
            notice={predictionResult.regulatory_notice}
          />

          <EnsembleMetrics metrics={predictionResult.ensemble_metrics} />

          <ModelResults modelResults={predictionResult.model_results} />

          <ShapExplanation shapData={predictionResult.shap_explanation} />
        </>
      )}
    </div>
  );
}
