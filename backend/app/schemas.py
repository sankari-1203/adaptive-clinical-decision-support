# Pydantic Schemas for Validation and Response
from typing import Literal, Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Patient Input Models
class DiabetesPatientInput(BaseModel):
    gender: Literal['Female', 'Male', 'Other'] = Field(..., description='Biological sex: Female, Male, or Other')
    age: float = Field(..., ge=1.0, le=120.0, description='Age in years (1 - 120)')
    hypertension: int = Field(..., ge=0, le=1, description='0 = No, 1 = Yes')
    heart_disease: int = Field(..., ge=0, le=1, description='0 = No, 1 = Yes')
    smoking_history: Literal['never', 'No Info', 'current', 'former', 'ever', 'not current'] = Field(
        ..., description='Smoking history category'
    )
    bmi: float = Field(..., ge=10.0, le=90.0, description='Body Mass Index (10.0 - 90.0)')
    HbA1c_level: float = Field(..., ge=3.0, le=16.0, description='Hemoglobin A1c level (3.0 - 16.0%)')
    blood_glucose_level: float = Field(..., ge=40.0, le=400.0, description='Blood glucose level in mg/dL (40 - 400)')

class CardioPatientInput(BaseModel):
    age_years: float = Field(..., ge=18.0, le=100.0, description='Age in years (18 - 100)')
    gender: int = Field(..., ge=1, le=2, description='Gender: 1 = Female, 2 = Male')
    height: float = Field(..., ge=100.0, le=250.0, description='Height in cm (100 - 250)')
    weight: float = Field(..., ge=30.0, le=250.0, description='Weight in kg (30 - 250)')
    ap_hi: float = Field(..., ge=60.0, le=240.0, description='Systolic blood pressure in mmHg (60 - 240)')
    ap_lo: float = Field(..., ge=40.0, le=160.0, description='Diastolic blood pressure in mmHg (40 - 160)')
    cholesterol: int = Field(..., ge=1, le=3, description='1 = Normal, 2 = Above Normal, 3 = Well Above Normal')
    gluc: int = Field(..., ge=1, le=3, description='1 = Normal, 2 = Above Normal, 3 = Well Above Normal')
    smoke: int = Field(..., ge=0, le=1, description='Smoking status: 0 = No, 1 = Yes')
    alco: int = Field(..., ge=0, le=1, description='Alcohol intake: 0 = No, 1 = Yes')
    active: int = Field(..., ge=0, le=1, description='Physical activity: 0 = No, 1 = Yes')

# Individual Model Result
class ModelResultItem(BaseModel):
    model: str
    prediction_label: str
    prediction_binary: int
    risk_probability: float
    risk_probability_pct: str
    confidence: float
    confidence_pct: str
    weight: float
    weight_pct: str

# Ensemble Metrics Response
class EnsembleMetricsResponse(BaseModel):
    disease_name: str
    final_prediction: int
    final_prediction_label: str
    risk_probability: float
    risk_probability_pct: str
    weighted_confidence: float
    weighted_confidence_pct: str
    agreement_score: float
    agreement_score_pct: str
    disagreement_score: float
    disagreement_score_pct: str
    vote_entropy: float
    vote_entropy_str: str
    uncertainty_score: float
    uncertainty_score_str: str
    probability_variance: float
    probability_variance_str: str
    reliability: str
    risk_category: str
    decision_title: str
    decision_subtitle: str
    clinical_recommendation: str

# SHAP Attribution Item
class ShapFeatureItem(BaseModel):
    feature: str
    patient_value: float
    shap_value: float
    absolute_shap: float
    direction: str

# SHAP Explanation Response
class ShapExplanationResponse(BaseModel):
    top_feature: str
    top_shap_value: float
    shap_summary: str
    feature_attributions: List[ShapFeatureItem]
    disclaimer: str

# Full Pipeline Prediction Response
class PredictionResponse(BaseModel):
    disease: str
    patient_data: Dict[str, Any]
    model_results: List[ModelResultItem]
    ensemble_metrics: EnsembleMetricsResponse
    shap_explanation: ShapExplanationResponse
    regulatory_notice: str

# API Health & Status Response
class HealthResponse(BaseModel):
    status: str
    version: str
    models_loaded: Dict[str, bool]
    details: Dict[str, Any]

# Disease Information Response
class DiseaseSchemaResponse(BaseModel):
    disease: str
    display_name: str
    features: List[str]
    sample_inputs: Dict[str, Any]
