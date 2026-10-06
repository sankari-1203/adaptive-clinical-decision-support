# Adaptive Clinical Decision Support System (CDSS)

[![Python 3.12](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React_18-61dafb.svg)](https://reactjs.org/)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/ML-XGBoost-brightgreen.svg)](https://xgboost.readthedocs.io/)
[![SHAP](https://img.shields.io/badge/XAI-SHAP-purple.svg)](https://shap.readthedocs.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Important Regulatory Notice:**  
> **For clinical decision support only. This prediction does not replace professional medical evaluation.**

---

## 1. Executive Summary & Architecture

The **Adaptive Clinical Decision Support System (CDSS)** is a production-grade software product engineered for dual-disease clinical risk assessment:
1. **Diabetes Mellitus** (8 clinical biomarkers)
2. **Cardiovascular Disease** (11 physiological & behavioral parameters)

Unlike naive machine learning classifiers that only output binary classifications or uncalibrated probabilities, this system incorporates:
- **Four Classical ML Models**: Logistic Regression, Support Vector Machine (SVM), Random Forest, and XGBoost.
- **F1-Score Weighted Ensembling**: Models are weighted based on validation F1 performance.
- **Model Disagreement & Consensus Tracking**: Quantifies inter-model consensus.
- **Shannon Vote Entropy**: Measures vote distribution spread ($H = -\sum p_k \log_2 p_k$).
- **Adaptive Uncertainty Quantification**: Combines ensemble confidence and vote entropy to classify cases into **HIGH**, **MEDIUM**, and **LOW** reliability tiers.
- **Local Explainable AI (SHAP)**: Uses TreeExplainer to attribute risk-increasing vs. protective factors for each patient.
- **Adaptive Support Recommendations**: Translates risk + reliability signals into clear clinical guidance.

---

## 2. Core Mathematical Formulations

### 2.1 F1-Score Derived Model Weights
Weights are computed from validation F1 scores and persisted in `model_weights.pkl`:
$$w_i = \frac{F1_i}{\sum_{j=1}^4 F1_j}$$

### 2.2 Weighted Ensemble Probability
$$P_{\text{ensemble}} = \sum_{i=1}^4 (w_i \times P_i)$$

### 2.3 Individual & Weighted Confidence
$$C_i = \max(P_i, 1 - P_i)$$
$$C_{\text{weighted}} = \sum_{i=1}^4 (w_i \times C_i)$$

### 2.4 Model Agreement & Disagreement
$$\text{Agreement} = \left(\frac{\text{Number of models supporting majority class}}{4}\right) \times 100$$
$$\text{Disagreement} = 100 - \text{Agreement}$$

### 2.5 Shannon Vote Entropy
For binary hard votes $p_k \in \{p_0, p_1\}$:
$$H = -\sum_{k \in \{0, 1\}} p_k \log_2(p_k) \quad \text{where } p_k \log_2(p_k) = 0 \text{ if } p_k = 0$$
- Unanimous (4-0): $H = 0.00$
- Split (3-1): $H = -(0.75 \log_2 0.75 + 0.25 \log_2 0.25) = 0.81$
- Tie (2-2): $H = 1.00$

### 2.6 Adaptive Uncertainty Quantification
$$U = \alpha (1 - C_{\text{weighted}}) + \beta \times H_{\text{norm}}$$
where $\alpha = 0.6$ and $\beta = 0.4$.

### 2.7 Reliability Stratification
- **HIGH Reliability**: $U < 0.30$
- **MEDIUM Reliability**: $0.30 \le U < 0.60$
- **LOW Reliability**: $U \ge 0.60$

---

## 3. Project Directory Structure

```text
ADAPTIVE CLINICAL DECISION/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # Lifespan startup, CORS, static mounting
│   │   ├── config.py            # Environment variables and thresholds
│   │   ├── schemas.py           # Pydantic input/response validation
│   │   ├── model_loader.py      # Artifact loader and singleton cache
│   │   ├── preprocessing.py     # Reproducible preprocessing pipelines
│   │   ├── predictor.py         # 4-model inference engine
│   │   ├── ensemble.py          # F1-weighted probability & agreement
│   │   ├── uncertainty.py       # Vote entropy & adaptive uncertainty
│   │   ├── explainability.py    # SHAP TreeExplainer & shape handling
│   │   ├── decision_engine.py   # Clinical wording synthesizer
│   │   └── routers/
│   │       ├── __init__.py
│   │       ├── health.py        # Health, diseases, model status APIs
│   │       └── prediction.py    # POST /api/predict/{disease}
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_artifacts.py
│   │   ├── test_preprocessing.py
│   │   ├── test_prediction.py
│   │   ├── test_ensemble.py
│   │   ├── test_uncertainty.py
│   │   ├── test_explainability.py
│   │   ├── test_api.py
│   │   └── test_notebook_comparison.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   ├── api/
│   │   │   └── predictionApi.js
│   │   ├── components/
│   │   │   ├── DiseaseSelector.jsx
│   │   │   ├── PatientForm.jsx
│   │   │   ├── ModelResults.jsx
│   │   │   ├── EnsembleMetrics.jsx
│   │   │   ├── DecisionCard.jsx
│   │   │   └── ShapExplanation.jsx
│   │   └── styles/
│   │       └── app.css
│   ├── dist/
│   │   └── index.html           # Standalone production web dashboard
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── models/
│   ├── Diabetes_Project/
│   │   ├── models/              # .pkl models, scaler, encoders
│   │   ├── results/             # model_evaluation.csv
│   │   ├── plots/
│   │   ├── shap/
│   │   ├── feature_columns.json
│   │   └── project_info.json
│   └── Cardiovascular_Project/
│       ├── models/              # .pkl models, scaler
│       ├── results/             # model_evaluation.csv
│       ├── plots/
│       ├── shap/
│       ├── feature_columns.json
│       └── project_info.json
├── docs/
│   └── api_docs.md
├── .env.example
├── .gitignore
├── run_backend.bat
└── README.md
```

---

## 4. Exact Artifacts Loaded

### Diabetes Pipeline (`models/Diabetes_Project/`)
- `models/scaler.pkl`: StandardScaler fitted on 8 features.
- `models/gender_encoder.pkl`: LabelEncoder for Biological Sex.
- `models/smoking_encoder.pkl`: LabelEncoder for Smoking History.
- `models/logistic_regression.pkl`: Trained Logistic Regression.
- `models/svm.pkl`: Trained Support Vector Classifier.
- `models/random_forest.pkl`: Trained Random Forest Classifier.
- `models/xgboost.pkl`: Trained XGBoost Classifier.
- `models/model_weights.pkl`: F1 weights `[0.23998, 0.23300, 0.26163, 0.26537]`.
- `feature_columns.json`: `['gender', 'age', 'hypertension', 'heart_disease', 'smoking_history', 'bmi', 'HbA1c_level', 'blood_glucose_level']`.

### Cardiovascular Pipeline (`models/Cardiovascular_Project/`)
- `models/scaler.pkl`: StandardScaler fitted on 11 features.
- `models/logistic_regression.pkl`: Trained Logistic Regression.
- `models/svm.pkl`: Trained Support Vector Classifier.
- `models/random_forest.pkl`: Trained Random Forest Classifier.
- `models/xgboost.pkl`: Trained XGBoost Classifier.
- `models/model_weights.pkl`: F1 weights `[0.24791, 0.24699, 0.24978, 0.25530]`.
- `feature_columns.json`: `['age_years', 'gender', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc', 'smoke', 'alco', 'active']`.

---

## 5. Quickstart & Execution Instructions

### Prerequisites
- Python 3.10+ (Tested on Python 3.12)
- Virtual environment with dependencies installed

### Option A: One-Click Launch (Windows)
Double-click `run_backend.bat` or run:
```cmd
cd "C:\ADAPTIVE CLINICAL DECISION"
run_backend.bat
```
Then open your browser at **`http://localhost:8000/`**. The interactive dashboard will load immediately!

### Option B: Manual Command Line
```powershell
# 1. Navigate to backend
cd "C:\ADAPTIVE CLINICAL DECISION\backend"

# 2. Activate virtual environment
& "d:\project 1\.venv\Scripts\Activate.ps1"

# 3. Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 6. Verification & Automated Test Results

The backend includes a comprehensive pytest suite covering all 12 testing specifications from Section 12 of the product documentation:

```powershell
pytest backend/tests -v
```

### Test Suite Output:
```text
tests/test_api.py::test_api_health PASSED                                [  4%]
tests/test_api.py::test_api_diseases PASSED                              [  9%]
tests/test_api.py::test_api_models_status PASSED                         [ 13%]
tests/test_api.py::test_api_predict_diabetes_success PASSED              [ 18%]
tests/test_api.py::test_api_predict_cardio_success PASSED                [ 22%]
tests/test_api.py::test_api_predict_invalid_input_rejected PASSED        [ 27%]
tests/test_api.py::test_no_retraining_called PASSED                      [ 31%]
tests/test_artifacts.py::test_diabetes_artifacts_load_successfully PASSED [ 36%]
tests/test_artifacts.py::test_cardiovascular_artifacts_load_successfully PASSED [ 40%]
tests/test_artifacts.py::test_missing_artifact_raises_clear_error PASSED [ 45%]
tests/test_ensemble.py::test_individual_confidences PASSED               [ 50%]
tests/test_ensemble.py::test_weighted_ensemble_metrics PASSED            [ 54%]
tests/test_explainability.py::test_diabetes_shap_explanation PASSED      [ 59%]
tests/test_explainability.py::test_cardio_shap_explanation PASSED        [ 63%]
tests/test_notebook_comparison.py::test_notebook_cardiovascular_sample_patient PASSED [ 68%]
tests/test_notebook_comparison.py::test_notebook_diabetes_sample_patient PASSED [ 72%]
tests/test_prediction.py::test_four_models_diabetes_prediction PASSED    [ 77%]
tests/test_prediction.py::test_four_models_cardio_prediction PASSED      [ 81%]
tests/test_preprocessing.py::test_diabetes_preprocessing PASSED          [ 86%]
tests/test_preprocessing.py::test_cardio_preprocessing PASSED            [ 90%]
tests/test_uncertainty.py::test_vote_entropy_values PASSED               [ 95%]
tests/test_uncertainty.py::test_uncertainty_quantification_reliability_tiers PASSED [100%]

======================= 22 passed, 5 warnings in 24.87s =======================
```

---

## 7. Notebook Comparison Validation

The application was benchmarked against the original Colab notebook (`cardiovascular_disease_adaptive_uncertainty_ensemble.py` Part 10 manual patient inference) using the identical sample patient:

| Parameter | Colab Training Notebook | Production Web Application | Status |
| :--- | :---: | :---: | :---: |
| **Input Feature Order** | Canonical 11 features | Canonical 11 features | **MATCH** |
| **Logistic Regression Pred / Prob** | 0 / 22.7% | 0 / 22.7% | **MATCH** |
| **SVM Pred / Prob** | 0 / 14.2% | 0 / 14.2% | **MATCH** |
| **Random Forest Pred / Prob** | 0 / 10.8% | 0 / 10.8% | **MATCH** |
| **XGBoost Pred / Prob** | 0 / 15.5% | 0 / 15.5% | **MATCH** |
| **Ensemble Risk Probability** | 15.8% | 15.8% | **MATCH** |
| **Model Agreement Score** | 100% | 100% | **MATCH** |
| **Vote Entropy (H)** | 0.00 | 0.00 | **MATCH** |
| **3-1 Split Vote Entropy** | 0.81 | 0.81 | **MATCH** |
| **Adaptive Uncertainty Score** | 0.09 | 0.09 | **MATCH** |
| **Reliability Classification** | HIGH | HIGH | **MATCH** |

---

## 8. Security & Privacy Guarantees

- **No Patient Feature Logging**: Patient clinical measurements are never persisted to disk or server logs.
- **No Third-Party AI Data Leaks**: Zero patient data is routed to external LLMs or third-party cloud inference services.
- **Internal Error Shielding**: Production exception handlers prevent exposing local filesystem paths or Python stack traces to browser clients.
- **No Model Retraining in API**: Models are purely frozen and loaded read-only at startup.
