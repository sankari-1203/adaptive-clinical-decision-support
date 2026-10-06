"""
Predictor Module
Runs inference across the four saved models (LR, SVM, RF, XGBoost)
and returns individual predictions and probabilities.
"""

from typing import Dict, Any, Tuple
import numpy as np
import pandas as pd
from app.config import MODEL_NAMES

def run_four_models(
    models: Dict[str, Any],
    patient_df: pd.DataFrame,
    patient_scaled: np.ndarray,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Executes inference on all 4 models:
    - Logistic Regression & SVM use patient_scaled
    - Random Forest & XGBoost use patient_df
    
    Returns:
        predictions: np.ndarray of shape (4,), binary predictions [LR, SVM, RF, XGB]
        probabilities: np.ndarray of shape (4,), positive class probabilities [LR, SVM, RF, XGB]
    """
    lr_model = models["Logistic Regression"]
    svm_model = models["SVM"]
    rf_model = models["Random Forest"]
    xgb_model = models["XGBoost"]

    # 1. Logistic Regression
    lr_pred = int(lr_model.predict(patient_scaled)[0])
    lr_prob = float(lr_model.predict_proba(patient_scaled)[0, 1])

    # 2. Support Vector Machine
    svm_pred = int(svm_model.predict(patient_scaled)[0])
    svm_prob = float(svm_model.predict_proba(patient_scaled)[0, 1])

    # 3. Random Forest
    rf_pred = int(rf_model.predict(patient_df)[0])
    rf_prob = float(rf_model.predict_proba(patient_df)[0, 1])

    # 4. XGBoost
    xgb_pred = int(xgb_model.predict(patient_df)[0])
    xgb_prob = float(xgb_model.predict_proba(patient_df)[0, 1])

    predictions = np.array([lr_pred, svm_pred, rf_pred, xgb_pred], dtype=int)
    probabilities = np.array([lr_prob, svm_prob, rf_prob, xgb_prob], dtype=float)

    return predictions, probabilities
