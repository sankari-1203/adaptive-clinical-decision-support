"""
Prediction Router
Handles POST /api/predict/{disease}
Executes complete ML pipeline:
Preprocessing -> Inference -> Weighted Ensemble -> Uncertainty -> SHAP -> Clinical Decision
"""

import logging
from typing import Dict, Any, Union
from fastapi import APIRouter, HTTPException, Request
from pydantic import ValidationError

from app.schemas import (
    DiabetesPatientInput,
    CardioPatientInput,
    PredictionResponse,
    EnsembleMetricsResponse,
    ShapExplanationResponse,
)
from app.model_loader import get_disease_artifacts, LOADED_ARTIFACTS
from app.preprocessing import preprocess_patient_diabetes, preprocess_patient_cardio
from app.predictor import run_four_models
from app.ensemble import calculate_ensemble_metrics
from app.uncertainty import quantify_uncertainty
from app.explainability import CDSSExplainer
from app.decision_engine import synthesize_clinical_decision
from app.config import REGULATORY_DISCLAIMER

logger = logging.getLogger("cdss.prediction")
router = APIRouter(prefix="/api", tags=["Prediction"])

# Cache SHAP explainers to avoid re-initializing on every request
SHAP_EXPLAINERS: Dict[str, CDSSExplainer] = {}

def get_or_create_explainer(disease: str, artifacts: Dict[str, Any]) -> CDSSExplainer:
    key = disease.lower()
    if key not in SHAP_EXPLAINERS:
        # Use Random Forest as the canonical tree explainer
        tree_model = artifacts["models"]["Random Forest"]
        features = artifacts["feature_columns"]
        SHAP_EXPLAINERS[key] = CDSSExplainer(tree_model, features, disease_name=artifacts["disease"])
    return SHAP_EXPLAINERS[key]

@router.post("/predict/{disease}")
async def predict_disease(disease: str, request: Request) -> Dict[str, Any]:
    """
    Complete prediction pipeline for specified disease ('diabetes' or 'cardiovascular').
    Never calls fit(), train(), or retraining.
    """
    disease_clean = disease.lower().strip()
    if disease_clean not in ["diabetes", "cardiovascular"]:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported disease '{disease}'. Must be 'diabetes' or 'cardiovascular'."
        )

    try:
        artifacts = get_disease_artifacts(disease_clean)
    except KeyError:
        raise HTTPException(
            status_code=503,
            detail=f"Models for disease '{disease}' are not loaded or initialized."
        )

    # 1. Parse and Validate Raw Payload with Pydantic
    try:
        raw_body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON request payload.")

    if disease_clean == "diabetes":
        try:
            validated_input = DiabetesPatientInput(**raw_body)
            patient_dict = validated_input.model_dump()
        except ValidationError as ve:
            raise HTTPException(
                status_code=422,
                detail=f"Validation failed for Diabetes input: {ve.errors()}"
            )
        patient_df, patient_scaled = preprocess_patient_diabetes(
            patient_dict,
            artifacts["gender_encoder"],
            artifacts["smoking_encoder"],
            artifacts["scaler"],
            artifacts["feature_columns"],
        )
    else:  # cardiovascular
        try:
            validated_input = CardioPatientInput(**raw_body)
            patient_dict = validated_input.model_dump()
        except ValidationError as ve:
            raise HTTPException(
                status_code=422,
                detail=f"Validation failed for Cardiovascular input: {ve.errors()}"
            )
        patient_df, patient_scaled = preprocess_patient_cardio(
            patient_dict,
            artifacts["scaler"],
            artifacts["feature_columns"],
        )

    # 2. Four Model Predictions
    predictions, probabilities = run_four_models(
        artifacts["models"],
        patient_df,
        patient_scaled,
    )

    # 3. Weighted Ensemble Calculations
    weights = artifacts["weights"]
    ensemble_res = calculate_ensemble_metrics(
        predictions,
        probabilities,
        weights,
        disease_name=artifacts["disease"]
    )

    # 4. Uncertainty Quantification
    uncertainty_res = quantify_uncertainty(
        predictions,
        probabilities,
        weighted_confidence=ensemble_res["weighted_confidence"],
    )

    # 5. Adaptive Decision Synthesis
    decision_res = synthesize_clinical_decision(
        disease_name=artifacts["disease"],
        final_prediction=ensemble_res["final_prediction"],
        risk_probability=ensemble_res["risk_probability"],
        weighted_confidence=ensemble_res["weighted_confidence"],
        agreement_score=ensemble_res["agreement_score"],
        disagreement_score=ensemble_res["disagreement_score"],
        uncertainty_score=uncertainty_res["uncertainty_score"],
        reliability=uncertainty_res["reliability"],
    )

    # 6. SHAP Explainability
    explainer = get_or_create_explainer(disease_clean, artifacts)
    shap_res = explainer.explain(patient_df)

    # 7. Assemble Full Response
    return {
        "disease": artifacts["disease"],
        "patient_data": patient_dict,
        "model_results": ensemble_res["model_results"],
        "ensemble_metrics": {
            "disease_name": artifacts["disease"],
            "final_prediction": ensemble_res["final_prediction"],
            "final_prediction_label": ensemble_res["final_prediction_label"],
            "risk_probability": ensemble_res["risk_probability"],
            "risk_probability_pct": ensemble_res["risk_probability_pct"],
            "weighted_confidence": ensemble_res["weighted_confidence"],
            "weighted_confidence_pct": ensemble_res["weighted_confidence_pct"],
            "agreement_score": ensemble_res["agreement_score"],
            "agreement_score_pct": ensemble_res["agreement_score_pct"],
            "disagreement_score": ensemble_res["disagreement_score"],
            "disagreement_score_pct": ensemble_res["disagreement_score_pct"],
            "vote_entropy": uncertainty_res["vote_entropy"],
            "vote_entropy_str": uncertainty_res["vote_entropy_str"],
            "uncertainty_score": uncertainty_res["uncertainty_score"],
            "uncertainty_score_str": uncertainty_res["uncertainty_score_str"],
            "probability_variance": uncertainty_res["probability_variance"],
            "probability_variance_str": uncertainty_res["probability_variance_str"],
            "reliability": uncertainty_res["reliability"],
            "risk_category": decision_res["risk_category"],
            "decision_title": decision_res["decision_title"],
            "decision_subtitle": decision_res["decision_subtitle"],
            "clinical_recommendation": decision_res["clinical_recommendation"],
        },
        "shap_explanation": shap_res,
        "regulatory_notice": REGULATORY_DISCLAIMER,
    }
