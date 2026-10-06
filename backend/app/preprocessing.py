"""
Preprocessing Module
Reproduces the exact training preprocessing and feature order for Diabetes and Cardiovascular pipelines.
No model training, fitting, or retraining occurs here.
"""

from typing import Dict, Any, Tuple, List
import pandas as pd
import numpy as np

def preprocess_patient_diabetes(
    patient_raw_dict: Dict[str, Any],
    gender_encoder,
    smoking_encoder,
    scaler,
    feature_columns: List[str]
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Preprocess raw patient input dictionary for Diabetes prediction.
    Applies categorical label encoding to gender and smoking_history,
    aligns features into the canonical training order, and scales for LR/SVM.
    Returns:
        patient_df: DataFrame with encoded values (for tree models: RF, XGBoost)
        patient_scaled: Scaled numpy array (for distance models: LR, SVM)
    """
    gender_val = str(patient_raw_dict["gender"])
    smoking_val = str(patient_raw_dict["smoking_history"])

    # Categorical encoding using saved encoders
    gender_encoded = int(gender_encoder.transform([gender_val])[0])
    smoking_encoded = int(smoking_encoder.transform([smoking_val])[0])

    row_data = {
        "gender": gender_encoded,
        "age": float(patient_raw_dict["age"]),
        "hypertension": int(patient_raw_dict["hypertension"]),
        "heart_disease": int(patient_raw_dict["heart_disease"]),
        "smoking_history": smoking_encoded,
        "bmi": float(patient_raw_dict["bmi"]),
        "HbA1c_level": float(patient_raw_dict["HbA1c_level"]),
        "blood_glucose_level": float(patient_raw_dict["blood_glucose_level"]),
    }

    # Strict column order alignment
    patient_df = pd.DataFrame([row_data], columns=feature_columns)

    # Scaling using saved StandardScaler
    patient_scaled = scaler.transform(patient_df)

    return patient_df, patient_scaled

def preprocess_patient_cardio(
    patient_raw_dict: Dict[str, Any],
    scaler,
    feature_columns: List[str]
) -> Tuple[pd.DataFrame, np.ndarray]:
    """
    Preprocess raw patient input dictionary for Cardiovascular prediction.
    Aligns numeric inputs into canonical training order and scales for LR/SVM.
    Returns:
        patient_df: DataFrame with raw values (for tree models: RF, XGBoost)
        patient_scaled: Scaled numpy array (for distance models: LR, SVM)
    """
    row_data = {col: float(patient_raw_dict[col]) for col in feature_columns}

    # Strict column order alignment
    patient_df = pd.DataFrame([row_data], columns=feature_columns)

    # Scaling using saved StandardScaler
    patient_scaled = scaler.transform(patient_df)

    return patient_df, patient_scaled
