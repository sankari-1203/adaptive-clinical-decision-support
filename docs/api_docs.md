# Adaptive Clinical Decision Support System - API Documentation

## Overview
The CDSS API provides production-grade endpoints for multi-model clinical risk prediction, uncertainty quantification, and SHAP-based feature attributions.

**Base URL**: `http://localhost:8000`  
**Interactive Swagger UI**: `http://localhost:8000/docs`  
**OpenAPI Specification**: `http://localhost:8000/openapi.json`

---

## 1. Health & Availability Check
### `GET /api/health`
Verifies backend status and model artifact readiness.

#### Response (200 OK)
```json
{
  "status": "healthy",
  "service": "Adaptive Clinical Decision Support System (CDSS)",
  "version": "1.0.0",
  "models_loaded": {
    "diabetes": true,
    "cardiovascular": true
  },
  "regulatory_notice": "For clinical decision support only. This prediction does not replace professional medical evaluation."
}
```

---

## 2. Available Disease Protocols
### `GET /api/diseases`
Returns supported disease protocols, active features, and input range specifications.

#### Response (200 OK)
```json
{
  "diseases": [
    {
      "id": "diabetes",
      "name": "Diabetes",
      "button_text": "PREDICT DIABETES RISK",
      "features": ["gender", "age", "hypertension", "heart_disease", "smoking_history", "bmi", "HbA1c_level", "blood_glucose_level"]
    },
    {
      "id": "cardiovascular",
      "name": "Cardiovascular",
      "button_text": "PREDICT CARDIOVASCULAR RISK",
      "features": ["age_years", "gender", "height", "weight", "ap_hi", "ap_lo", "cholesterol", "gluc", "smoke", "alco", "active"]
    }
  ]
}
```

---

## 3. Disease Model Status
### `GET /api/models/{disease}`
Returns the four loaded models, F1-derived weights, and validation benchmarks.

#### Parameters
- `disease` (path): `diabetes` or `cardiovascular`

---

## 4. Run Clinical Prediction Pipeline
### `POST /api/predict/{disease}`
Executes the end-to-end ML pipeline: Preprocessing → 4-Model Inference → Weighted Ensemble → Uncertainty Quantification → SHAP Local Attribution → Adaptive Decision Synthesis.

#### Diabetes Payload Example
```json
{
  "gender": "Female",
  "age": 45.0,
  "hypertension": 0,
  "heart_disease": 0,
  "smoking_history": "never",
  "bmi": 25.4,
  "HbA1c_level": 5.8,
  "blood_glucose_level": 110.0
}
```

#### Cardiovascular Payload Example
```json
{
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
  "active": 1
}
```

#### Response Structure (200 OK)
- `disease`: Disease name
- `model_results`: Individual predictions, positive class probabilities, confidences, and F1 weights for LR, SVM, RF, and XGBoost
- `ensemble_metrics`:
  - `risk_probability_pct`: Weighted probability $\sum w_i P_i$
  - `agreement_score_pct`: $(\text{majority models} / 4) \times 100$
  - `disagreement_score_pct`: $100 - \text{agreement}$
  - `weighted_confidence_pct`: $\sum w_i \max(P_i, 1 - P_i)$
  - `vote_entropy_str`: Safe binary entropy $H = -\sum p_k \log_2(p_k)$
  - `uncertainty_score_str`: $0.6 \times (1 - C_{\text{weighted}}) + 0.4 \times H$
  - `reliability`: `HIGH`, `MEDIUM`, or `LOW`
  - `decision_title` & `clinical_recommendation`
- `shap_explanation`:
  - `top_feature`: Strongest biomarker
  - `top_shap_value`: Attribution magnitude
  - `shap_summary`: Natural language narrative
  - `feature_attributions`: Ranked array of features with direction and patient values
  - `disclaimer`: Regulatory non-causality notice
- `regulatory_notice`: Mandatory clinical decision support disclaimer
