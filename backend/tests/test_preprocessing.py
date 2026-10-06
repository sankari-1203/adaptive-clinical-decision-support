"""
Preprocessing Tests
Verifies exact saved encoders, scalers, and canonical feature ordering.
"""

import numpy as np
import pandas as pd
from app.model_loader import load_diabetes_artifacts, load_cardio_artifacts
from app.preprocessing import preprocess_patient_diabetes, preprocess_patient_cardio

def test_diabetes_preprocessing():
    artifacts = load_diabetes_artifacts()
    patient_raw = {
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
        patient_raw,
        artifacts["gender_encoder"],
        artifacts["smoking_encoder"],
        artifacts["scaler"],
        artifacts["feature_columns"],
    )
    assert list(patient_df.columns) == artifacts["feature_columns"]
    assert patient_scaled.shape == (1, 8)
    # Check that gender 'Female' was encoded to a numeric value
    assert isinstance(patient_df["gender"].iloc[0], (int, np.integer))

def test_cardio_preprocessing():
    artifacts = load_cardio_artifacts()
    patient_raw = {
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
        patient_raw,
        artifacts["scaler"],
        artifacts["feature_columns"],
    )
    assert list(patient_df.columns) == artifacts["feature_columns"]
    assert patient_scaled.shape == (1, 11)
