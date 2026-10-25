"""
Model Loader Module
Loads and caches disease-specific models, scalers, encoders, and weights once at startup.
Never calls fit() or retraining. Fails with clear errors if any artifact is missing.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
import joblib
import numpy as np
import pandas as pd

from app.config import DIABETES_MODELS_DIR, CARDIO_MODELS_DIR

logger = logging.getLogger("cdss.model_loader")

LOADED_ARTIFACTS: Dict[str, Dict[str, Any]] = {}

def _resolve_artifact(directory: Path, filename: str) -> Path:
    # First check directory itself (direct or .gz)
    direct_path = directory / filename
    if direct_path.exists():
        return direct_path
    gz_path = directory / f"{filename}.gz"
    if gz_path.exists():
        return gz_path

    # Check models/ subfolder (direct or .gz)
    sub_path = directory / "models" / filename
    if sub_path.exists():
        return sub_path
    sub_gz_path = directory / "models" / f"{filename}.gz"
    if sub_gz_path.exists():
        return sub_gz_path

    # Check results/ subfolder (for csv)
    res_path = directory / "results" / filename
    if res_path.exists():
        return res_path
    raise FileNotFoundError(f"Required artifact '{filename}' (or '{filename}.gz') not found in {directory}")

def load_diabetes_artifacts(models_dir: Path = DIABETES_MODELS_DIR) -> Dict[str, Any]:
    logger.info(f"Loading Diabetes model artifacts from {models_dir}...")
    if not models_dir.exists():
        raise FileNotFoundError(f"Diabetes models directory does not exist: {models_dir}")

    scaler_path = _resolve_artifact(models_dir, "scaler.pkl")
    gender_enc_path = _resolve_artifact(models_dir, "gender_encoder.pkl")
    smoking_enc_path = _resolve_artifact(models_dir, "smoking_encoder.pkl")
    lr_path = _resolve_artifact(models_dir, "logistic_regression.pkl")
    svm_path = _resolve_artifact(models_dir, "svm.pkl")
    rf_path = _resolve_artifact(models_dir, "random_forest.pkl")
    xgb_path = _resolve_artifact(models_dir, "xgboost.pkl")
    weights_path = _resolve_artifact(models_dir, "model_weights.pkl")
    features_path = _resolve_artifact(models_dir, "feature_columns.json")
    eval_path = _resolve_artifact(models_dir, "model_evaluation.csv")

    scaler = joblib.load(scaler_path)
    gender_enc = joblib.load(gender_enc_path)
    smoking_enc = joblib.load(smoking_enc_path)
    lr_model = joblib.load(lr_path)
    svm_model = joblib.load(svm_path)
    rf_model = joblib.load(rf_path)
    xgb_model = joblib.load(xgb_path)

    with open(features_path, "r", encoding="utf-8") as f:
        feature_columns = json.load(f)

    weights_df = joblib.load(weights_path)
    weights = np.array(weights_df["Weight"], dtype=float)

    eval_df = pd.read_csv(eval_path)

    artifacts = {
        "disease": "Diabetes",
        "scaler": scaler,
        "gender_encoder": gender_enc,
        "smoking_encoder": smoking_enc,
        "models": {
            "Logistic Regression": lr_model,
            "SVM": svm_model,
            "Random Forest": rf_model,
            "XGBoost": xgb_model,
        },
        "feature_columns": feature_columns,
        "weights": weights,
        "evaluation": eval_df.to_dict(orient="records"),
    }
    logger.info("Diabetes artifacts loaded successfully.")
    return artifacts

def load_cardio_artifacts(models_dir: Path = CARDIO_MODELS_DIR) -> Dict[str, Any]:
    logger.info(f"Loading Cardiovascular model artifacts from {models_dir}...")
    if not models_dir.exists():
        raise FileNotFoundError(f"Cardiovascular models directory does not exist: {models_dir}")

    scaler_path = _resolve_artifact(models_dir, "scaler.pkl")
    lr_path = _resolve_artifact(models_dir, "logistic_regression.pkl")
    svm_path = _resolve_artifact(models_dir, "svm.pkl")
    rf_path = _resolve_artifact(models_dir, "random_forest.pkl")
    xgb_path = _resolve_artifact(models_dir, "xgboost.pkl")
    weights_path = _resolve_artifact(models_dir, "model_weights.pkl")
    features_path = _resolve_artifact(models_dir, "feature_columns.json")
    eval_path = _resolve_artifact(models_dir, "model_evaluation.csv")

    scaler = joblib.load(scaler_path)
    lr_model = joblib.load(lr_path)
    svm_model = joblib.load(svm_path)
    rf_model = joblib.load(rf_path)
    xgb_model = joblib.load(xgb_path)

    with open(features_path, "r", encoding="utf-8") as f:
        feature_columns = json.load(f)

    weights_df = joblib.load(weights_path)
    weights = np.array(weights_df["Weight"], dtype=float)

    eval_df = pd.read_csv(eval_path)

    artifacts = {
        "disease": "Cardiovascular",
        "scaler": scaler,
        "models": {
            "Logistic Regression": lr_model,
            "SVM": svm_model,
            "Random Forest": rf_model,
            "XGBoost": xgb_model,
        },
        "feature_columns": feature_columns,
        "weights": weights,
        "evaluation": eval_df.to_dict(orient="records"),
    }
    logger.info("Cardiovascular artifacts loaded successfully.")
    return artifacts

def load_all_artifacts() -> Dict[str, Dict[str, Any]]:
    global LOADED_ARTIFACTS
    LOADED_ARTIFACTS["diabetes"] = load_diabetes_artifacts()
    LOADED_ARTIFACTS["cardiovascular"] = load_cardio_artifacts()
    return LOADED_ARTIFACTS

def get_disease_artifacts(disease: str) -> Dict[str, Any]:
    key = disease.lower().strip()
    if key not in LOADED_ARTIFACTS:
        raise KeyError(f"No loaded artifacts for disease: {disease}. Loaded: {list(LOADED_ARTIFACTS.keys())}")
    return LOADED_ARTIFACTS[key]
