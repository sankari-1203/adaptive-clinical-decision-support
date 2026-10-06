"""
Notebook Comparison Tests
Verifies that the application reproduces the exact results from the Colab training notebook
using the same artifacts and preprocessing.
"""

from app.model_loader import load_cardio_artifacts, load_diabetes_artifacts
from app.preprocessing import preprocess_patient_cardio, preprocess_patient_diabetes
from app.predictor import run_four_models
from app.ensemble import calculate_ensemble_metrics
from app.uncertainty import quantify_uncertainty

def test_notebook_cardiovascular_sample_patient():
    """
    Validates the exact sample patient inputs from Colab Part 10:
    Age: 50.4, Gender: 1, Height: 168, Weight: 62, AP_HI: 110, AP_LO: 80,
    Chol: 1, Gluc: 1, Smoke: 0, Alco: 0, Active: 1.
    """
    artifacts = load_cardio_artifacts()
    patient = {
        "age_years": 50.4,
        "gender": 1,
        "height": 168.0,
        "weight": 62.0,
        "ap_hi": 110.0,
        "ap_lo": 80.0,
        "cholesterol": 1,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1,
    }

    patient_df, patient_scaled = preprocess_patient_cardio(
        patient, artifacts["scaler"], artifacts["feature_columns"]
    )
    preds, probs = run_four_models(artifacts["models"], patient_df, patient_scaled)

    # In the reference notebook, all four models predict 0 (low risk)
    assert all(p == 0 for p in preds)

    # Ensemble calculations
    ens = calculate_ensemble_metrics(preds, probs, artifacts["weights"], "Cardiovascular")
    assert ens["final_prediction"] == 0
    assert ens["agreement_score_pct"] == "100%"
    assert ens["disagreement_score_pct"] == "0%"

    # Uncertainty calculations
    unc = quantify_uncertainty(preds, probs, ens["weighted_confidence"])
    assert unc["vote_entropy_str"] == "0.00"
    assert unc["reliability"] == "HIGH"

def test_notebook_diabetes_sample_patient():
    """
    Validates a typical diabetes patient profile through the pipeline.
    """
    artifacts = load_diabetes_artifacts()
    patient = {
        "gender": "Female",
        "age": 45.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 25.4,
        "HbA1c_level": 5.8,
        "blood_glucose_level": 110.0,
    }

    patient_df, patient_scaled = preprocess_patient_diabetes(
        patient,
        artifacts["gender_encoder"],
        artifacts["smoking_encoder"],
        artifacts["scaler"],
        artifacts["feature_columns"],
    )
    preds, probs = run_four_models(artifacts["models"], patient_df, patient_scaled)

    assert len(preds) == 4
    assert len(probs) == 4
    ens = calculate_ensemble_metrics(preds, probs, artifacts["weights"], "Diabetes")
    assert "risk_probability" in ens
    assert "weighted_confidence" in ens
