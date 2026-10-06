"""
Explainability (SHAP) Tests
Verifies that SHAP tree explainers handle multi-dimensional arrays (such as (1, 11, 2)),
return ranked feature attributions, and include appropriate non-causal clinical disclaimers.
"""

import pandas as pd
from app.model_loader import load_diabetes_artifacts, load_cardio_artifacts
from app.explainability import CDSSExplainer, SHAP_DISCLAIMER

def test_diabetes_shap_explanation():
    artifacts = load_diabetes_artifacts()
    rf_model = artifacts["models"]["Random Forest"]
    features = artifacts["feature_columns"]

    explainer = CDSSExplainer(rf_model, features, disease_name="Diabetes")

    # Single patient dataframe
    patient_df = pd.DataFrame([{
        "gender": 0,
        "age": 55.0,
        "hypertension": 1,
        "heart_disease": 0,
        "smoking_history": 3,
        "bmi": 32.5,
        "HbA1c_level": 7.2,
        "blood_glucose_level": 180.0,
    }], columns=features)

    res = explainer.explain(patient_df)
    assert "top_feature" in res
    assert "top_shap_value" in res
    assert "feature_attributions" in res
    assert len(res["feature_attributions"]) <= len(features)
    assert res["disclaimer"] == SHAP_DISCLAIMER

def test_cardio_shap_explanation():
    artifacts = load_cardio_artifacts()
    rf_model = artifacts["models"]["Random Forest"]
    features = artifacts["feature_columns"]

    explainer = CDSSExplainer(rf_model, features, disease_name="Cardiovascular")

    patient_df = pd.DataFrame([{
        "age_years": 50.0,
        "gender": 1,
        "height": 165.0,
        "weight": 70.0,
        "ap_hi": 130.0,
        "ap_lo": 85.0,
        "cholesterol": 2,
        "gluc": 1,
        "smoke": 0,
        "alco": 0,
        "active": 1,
    }], columns=features)

    res = explainer.explain(patient_df)
    assert res["top_feature"] in features
    assert len(res["feature_attributions"]) == len(features)
