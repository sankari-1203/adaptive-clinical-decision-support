"""
Explainability Module (SHAP)
Generates local feature attribution using SHAP TreeExplainer on tree models.
Handles multi-dimensional array shapes dynamically, including (1, N, 2) or list of classes.
Includes regulatory disclaimer: SHAP explains model behavior, not medical causation.
"""

from typing import Dict, Any, List, Optional
import numpy as np
import pandas as pd
import shap

SHAP_DISCLAIMER = (
    "SHAP attributions explain model behavior on this input; "
    "they do not constitute clinical proof that a feature caused disease."
)

class CDSSExplainer:
    """SHAP explainer for clinical tree-based decision models."""

    def __init__(self, tree_model, feature_names: List[str], disease_name: str = "Diabetes"):
        self.model = tree_model
        self.feature_names = feature_names
        self.disease_name = disease_name
        self.explainer = shap.TreeExplainer(tree_model)

    def explain(self, patient_df: pd.DataFrame, max_features: Optional[int] = None) -> Dict[str, Any]:
        """
        Calculates SHAP values for a single patient record.
        Dynamically handles output shapes:
        - 3D array: shape (samples, features, classes) e.g., (1, 11, 2) -> extracts class 1
        - list: [class_0_array, class_1_array] -> extracts class 1
        - 2D array: shape (samples, features) -> extracts row 0
        """
        shap_raw = self.explainer.shap_values(patient_df)

        if isinstance(shap_raw, list):
            if len(shap_raw) >= 2:
                patient_shap = np.array(shap_raw[1])[0]
            else:
                patient_shap = np.array(shap_raw[0])[0]
        elif isinstance(shap_raw, np.ndarray):
            if shap_raw.ndim == 3:
                # Shape (samples, features, classes) e.g. (1, 11, 2) -> class 1
                patient_shap = shap_raw[0, :, 1]
            elif shap_raw.ndim == 2:
                # Shape (samples, features)
                patient_shap = shap_raw[0]
            else:
                patient_shap = shap_raw.flatten()
        else:
            patient_shap = np.array(shap_raw).flatten()

        patient_vals = patient_df.iloc[0].values

        rows = []
        for feat, val, s_val in zip(self.feature_names, patient_vals, patient_shap):
            s_float = float(s_val)
            direction = "Risk-Increasing" if s_float > 0 else "Protective"
            rows.append({
                "feature": str(feat),
                "patient_value": float(val),
                "shap_value": s_float,
                "absolute_shap": abs(s_float),
                "direction": direction,
            })

        # Sort features by absolute attribution
        sorted_rows = sorted(rows, key=lambda x: x["absolute_shap"], reverse=True)
        top_row = sorted_rows[0]
        top_feature = top_row["feature"]
        top_shap_value = top_row["shap_value"]

        if top_shap_value > 0:
            shap_summary = (
                f"{top_feature} (patient value: {top_row['patient_value']}) was the strongest factor "
                f"increasing the predicted risk of {self.disease_name.lower()}."
            )
        else:
            shap_summary = (
                f"{top_feature} (patient value: {top_row['patient_value']}) was the strongest protective factor "
                f"reducing the predicted risk of {self.disease_name.lower()}."
            )

        attributions = sorted_rows[:max_features] if max_features is not None else sorted_rows

        return {
            "top_feature": top_feature,
            "top_shap_value": float(top_shap_value),
            "shap_summary": shap_summary,
            "feature_attributions": attributions,
            "disclaimer": SHAP_DISCLAIMER,
        }
