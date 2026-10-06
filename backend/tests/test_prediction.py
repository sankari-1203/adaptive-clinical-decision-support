"""
Four-Model Prediction Tests
Verifies that all four saved models produce valid predictions and probabilities
without any model retraining.
"""

from app.model_loader import load_diabetes_artifacts, load_cardio_artifacts
from app.preprocessing import preprocess_patient_diabetes, preprocess_patient_cardio
from app.predictor import run_four_models

def test_four_models_diabetes_prediction():
    artifacts = load_diabetes_artifacts()
    patient_raw = {
        "gender": "Female",
        "age": 55.0,
        "hypertension": 1,
        "heart_disease": 0,
        "smoking_history": "former",
        "bmi": 32.5,
        "HbA1c_level": 7.2,
        "blood_glucose_level": 180.0,
    }
    patient_df, patient_scaled = preprocess_patient_diabetes(
        patient_raw,
        artifacts["gender_encoder"],
        artifacts["smoking_encoder"],
        artifacts["scaler"],
        artifacts["feature_columns"],
    )
    preds, probs = run_four_models(artifacts["models"], patient_df, patient_scaled)
    assert len(preds) == 4
    assert len(probs) == 4
    for p in preds:
        assert p in (0, 1)
    for pr in probs:
        assert 0.0 <= pr <= 1.0

def test_four_models_cardio_prediction():
    artifacts = load_cardio_artifacts()
    patient_raw = {
        "age_years": 62.0,
        "gender": 2,
        "height": 172.0,
        "weight": 85.0,
        "ap_hi": 150.0,
        "ap_lo": 95.0,
        "cholesterol": 3,
        "gluc": 2,
        "smoke": 1,
        "alco": 1,
        "active": 0,
    }
    patient_df, patient_scaled = preprocess_patient_cardio(
        patient_raw,
        artifacts["scaler"],
        artifacts["feature_columns"],
    )
    preds, probs = run_four_models(artifacts["models"], patient_df, patient_scaled)
    assert len(preds) == 4
    assert len(probs) == 4
    for p in preds:
        assert p in (0, 1)
    for pr in probs:
        assert 0.0 <= pr <= 1.0
