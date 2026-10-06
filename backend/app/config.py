# System Configuration
import os
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

DEFAULT_DIABETES_DIR = PROJECT_ROOT / 'models' / 'Diabetes_Project'
DEFAULT_CARDIO_DIR = PROJECT_ROOT / 'models' / 'Cardiovascular_Project'

DIABETES_MODELS_DIR = Path(os.getenv('DIABETES_MODELS_DIR', str(DEFAULT_DIABETES_DIR)))
CARDIO_MODELS_DIR = Path(os.getenv('CARDIO_MODELS_DIR', str(DEFAULT_CARDIO_DIR)))

API_HOST = os.getenv('API_HOST', '0.0.0.0')
API_PORT = int(os.getenv('API_PORT', '8000'))
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

MODEL_NAMES = [
    'Logistic Regression',
    'SVM',
    'Random Forest',
    'XGBoost'
]

UNCERTAINTY_ALPHA = float(os.getenv('UNCERTAINTY_ALPHA', '0.6'))
UNCERTAINTY_BETA = float(os.getenv('UNCERTAINTY_BETA', '0.4'))

RELIABILITY_HIGH_THRESHOLD = 0.30
RELIABILITY_MEDIUM_THRESHOLD = 0.60
DISAGREEMENT_LOW_THRESHOLD = 0.25

RISK_HIGH_THRESHOLD = 0.70
RISK_MODERATE_THRESHOLD = 0.50

DIABETES_FEATURES = [
    'gender',
    'age',
    'hypertension',
    'heart_disease',
    'smoking_history',
    'bmi',
    'HbA1c_level',
    'blood_glucose_level'
]

CARDIO_FEATURES = [
    'age_years',
    'gender',
    'height',
    'weight',
    'ap_hi',
    'ap_lo',
    'cholesterol',
    'gluc',
    'smoke',
    'alco',
    'active'
]

REGULATORY_DISCLAIMER = (
    'For clinical decision support only. This prediction does not replace professional medical evaluation.'
)
