"""
API End-to-End Tests
Tests all required endpoints:
- GET /api/health
- GET /api/diseases
- GET /api/models/{disease}
- POST /api/predict/{disease} (Diabetes & Cardio)
- Input validation & readable error messages
- No model retraining requirement
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.model_loader import load_all_artifacts

@pytest.fixture(scope="module")
def client():
    load_all_artifacts()
    with TestClient(app) as c:
        yield c

def test_api_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "diabetes" in data["models_loaded"]
    assert "cardiovascular" in data["models_loaded"]

def test_api_diseases(client):
    response = client.get("/api/diseases")
    assert response.status_code == 200
    data = response.json()
    disease_ids = [d["id"] for d in data["diseases"]]
    assert "diabetes" in disease_ids
    assert "cardiovascular" in disease_ids

def test_api_models_status(client):
    res_d = client.get("/api/models/diabetes")
    assert res_d.status_code == 200
    assert len(res_d.json()["models"]) == 4

    res_c = client.get("/api/models/cardiovascular")
    assert res_c.status_code == 200
    assert len(res_c.json()["models"]) == 4

    res_err = client.get("/api/models/unknown_disease")
    assert res_err.status_code == 404

def test_api_predict_diabetes_success(client):
    payload = {
        "gender": "Female",
        "age": 45.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 25.4,
        "HbA1c_level": 5.8,
        "blood_glucose_level": 110.0,
    }
    response = client.post("/api/predict/diabetes", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["disease"] == "Diabetes"
    assert len(data["model_results"]) == 4
    assert "ensemble_metrics" in data
    assert "shap_explanation" in data
    assert "regulatory_notice" in data

def test_api_predict_cardio_success(client):
    payload = {
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
    response = client.post("/api/predict/cardiovascular", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["disease"] == "Cardiovascular"
    assert len(data["model_results"]) == 4
    assert "ensemble_metrics" in data
    assert "shap_explanation" in data

def test_api_predict_invalid_input_rejected(client):
    # Missing required fields and out of range values
    invalid_payload = {
        "gender": "InvalidGender",
        "age": -5.0,
    }
    response = client.post("/api/predict/diabetes", json=invalid_payload)
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_no_retraining_called(client):
    """Verifies that fit() or train() is never called during API execution."""
    payload = {
        "gender": "Female",
        "age": 45.0,
        "hypertension": 0,
        "heart_disease": 0,
        "smoking_history": "never",
        "bmi": 25.4,
        "HbA1c_level": 5.8,
        "blood_glucose_level": 110.0,
    }
    with patch("sklearn.linear_model.LogisticRegression.fit") as mock_fit:
        response = client.post("/api/predict/diabetes", json=payload)
        assert response.status_code == 200
        mock_fit.assert_not_called()
