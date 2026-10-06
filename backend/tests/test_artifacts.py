"""
Artifact Loading Tests
Verifies that all required artifacts for Diabetes and Cardiovascular are loaded,
and that missing files raise a descriptive error without falling back to dummy models.
"""

import pytest
from pathlib import Path
from app.model_loader import load_diabetes_artifacts, load_cardio_artifacts, _resolve_artifact
from app.config import DIABETES_MODELS_DIR, CARDIO_MODELS_DIR

def test_diabetes_artifacts_load_successfully():
    artifacts = load_diabetes_artifacts(DIABETES_MODELS_DIR)
    assert artifacts["disease"] == "Diabetes"
    assert "scaler" in artifacts
    assert "gender_encoder" in artifacts
    assert "smoking_encoder" in artifacts
    assert len(artifacts["models"]) == 4
    assert set(artifacts["models"].keys()) == {
        "Logistic Regression", "SVM", "Random Forest", "XGBoost"
    }
    assert len(artifacts["feature_columns"]) == 8
    assert len(artifacts["weights"]) == 4
    assert abs(sum(artifacts["weights"]) - 1.0) < 1e-4

def test_cardiovascular_artifacts_load_successfully():
    artifacts = load_cardio_artifacts(CARDIO_MODELS_DIR)
    assert artifacts["disease"] == "Cardiovascular"
    assert "scaler" in artifacts
    assert len(artifacts["models"]) == 4
    assert set(artifacts["models"].keys()) == {
        "Logistic Regression", "SVM", "Random Forest", "XGBoost"
    }
    assert len(artifacts["feature_columns"]) == 11
    assert len(artifacts["weights"]) == 4
    assert abs(sum(artifacts["weights"]) - 1.0) < 1e-4

def test_missing_artifact_raises_clear_error(tmp_path):
    empty_dir = tmp_path / "empty_models"
    empty_dir.mkdir()
    with pytest.raises(FileNotFoundError) as exc_info:
        load_diabetes_artifacts(empty_dir)
    assert "scaler.pkl" in str(exc_info.value)
