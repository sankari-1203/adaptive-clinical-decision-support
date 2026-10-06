"""
Health & Metadata Router
Provides endpoints for health checks, model status, and disease schemas.
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.model_loader import LOADED_ARTIFACTS, get_disease_artifacts
from app.config import REGULATORY_DISCLAIMER

router = APIRouter(prefix="/api", tags=["System & Metadata"])

@router.get("/health")
def health_check() -> Dict[str, Any]:
    """Backend and model availability check."""
    loaded = {k: True for k in LOADED_ARTIFACTS.keys()}
    all_ready = "diabetes" in loaded and "cardiovascular" in loaded
    return {
        "status": "healthy" if all_ready else "degraded",
        "service": "Adaptive Clinical Decision Support System (CDSS)",
        "version": "1.0.0",
        "models_loaded": loaded,
        "regulatory_notice": REGULATORY_DISCLAIMER,
    }

@router.get("/diseases")
def get_available_diseases() -> Dict[str, Any]:
    """Returns available disease prediction pipelines and feature specifications."""
    return {
        "diseases": [
            {
                "id": "diabetes",
                "name": "Diabetes",
                "button_text": "PREDICT DIABETES RISK",
                "features": [
                    "gender", "age", "hypertension", "heart_disease",
                    "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"
                ],
                "categorical_fields": {
                    "gender": ["Female", "Male", "Other"],
                    "smoking_history": ["never", "No Info", "current", "former", "ever", "not current"],
                },
                "numeric_ranges": {
                    "age": {"min": 1, "max": 120, "default": 45},
                    "hypertension": {"options": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}]},
                    "heart_disease": {"options": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}]},
                    "bmi": {"min": 10.0, "max": 90.0, "default": 25.4},
                    "HbA1c_level": {"min": 3.0, "max": 16.0, "default": 5.8},
                    "blood_glucose_level": {"min": 40, "max": 400, "default": 110},
                }
            },
            {
                "id": "cardiovascular",
                "name": "Cardiovascular",
                "button_text": "PREDICT CARDIOVASCULAR RISK",
                "features": [
                    "age_years", "gender", "height", "weight", "ap_hi", "ap_lo",
                    "cholesterol", "gluc", "smoke", "alco", "active"
                ],
                "categorical_fields": {
                    "gender": [{"label": "Female", "value": 1}, {"label": "Male", "value": 2}],
                    "cholesterol": [
                        {"label": "Normal", "value": 1},
                        {"label": "Above Normal", "value": 2},
                        {"label": "Well Above Normal", "value": 3}
                    ],
                    "gluc": [
                        {"label": "Normal", "value": 1},
                        {"label": "Above Normal", "value": 2},
                        {"label": "Well Above Normal", "value": 3}
                    ],
                    "smoke": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                    "alco": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                    "active": [{"label": "No", "value": 0}, {"label": "Yes", "value": 1}],
                },
                "numeric_ranges": {
                    "age_years": {"min": 18, "max": 100, "default": 50.4},
                    "height": {"min": 100, "max": 250, "default": 168.0},
                    "weight": {"min": 30, "max": 250, "default": 62.0},
                    "ap_hi": {"min": 60, "max": 240, "default": 110.0},
                    "ap_lo": {"min": 40, "max": 160, "default": 80.0},
                }
            }
        ]
    }

@router.get("/models/{disease}")
def get_model_status(disease: str) -> Dict[str, Any]:
    """Loaded model status and evaluation metrics for the selected disease."""
    try:
        artifacts = get_disease_artifacts(disease)
    except KeyError:
        raise HTTPException(
            status_code=404,
            detail=f"Disease '{disease}' not found. Supported: {list(LOADED_ARTIFACTS.keys())}"
        )

    return {
        "disease": artifacts["disease"],
        "models": list(artifacts["models"].keys()),
        "weights": artifacts["weights"].tolist(),
        "feature_columns": artifacts["feature_columns"],
        "evaluation": artifacts["evaluation"],
    }
