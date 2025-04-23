# backend/serve_model.py
"""Utilitaires de chargement + prédiction + SHAP pour l’API FastAPI."""

import joblib
import pandas as pd
import shap
from pathlib import Path
from typing import Dict
from sklearn.base import BaseEstimator

# Chemin du pipeline entraîné
MODEL_PATH = Path(__file__).parent / "model" / "pipeline.pkl"

# Ordre officiel des 5 features
FEATURES_ORDER = [
    "EXT_SOURCE_1",
    "EXT_SOURCE_2",
    "EXT_SOURCE_3",
    "DAYS_BIRTH",
    "AMT_INCOME_TOTAL",
]

# ------------------------------------------------------------------
# 1) Chargement du pipeline
# ------------------------------------------------------------------

def load_pipeline() -> BaseEstimator:
    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"pipeline.pkl introuvable : {MODEL_PATH}. Exécute train_pipeline.py."
        )
    return joblib.load(MODEL_PATH)

# ------------------------------------------------------------------
# 2) Helpers
# ------------------------------------------------------------------

def _dict_to_df(features: Dict[str, float]) -> pd.DataFrame:
    """Transforme le dict reçu par l’API en DataFrame (1 ligne)."""
    missing = set(FEATURES_ORDER) - set(features)
    extra = set(features) - set(FEATURES_ORDER)
    if missing or extra:
        raise ValueError(
            f"Payload invalide. Manquants : {missing} ; en trop : {extra}"
        )
    row = [features[col] for col in FEATURES_ORDER]
    return pd.DataFrame([row], columns=FEATURES_ORDER)

# ------------------------------------------------------------------
# 3) Probabilité
# ------------------------------------------------------------------

def predict_proba(pipeline: BaseEstimator, features: Dict[str, float]) -> float:
    X_df = _dict_to_df(features)
    return float(pipeline.predict_proba(X_df)[0, 1])  # proba classe positive

# ------------------------------------------------------------------
# 4) Explication SHAP (TreeExplainer)
# ------------------------------------------------------------------

def explain_prediction(
    pipeline: BaseEstimator,
    features: Dict[str, float],
    max_feats: int = 5,
) -> Dict[str, float]:
    try:
        X_df = _dict_to_df(features)
        X_trans = pipeline.named_steps["preproc"].transform(X_df)
        explainer = shap.TreeExplainer(
            pipeline.named_steps["clf"], model_output="probability"
        )
        shap_vals = explainer.shap_values(X_trans)[1]  # classe positive
        contribs = {
            FEATURES_ORDER[i]: float(shap_vals[0][i])
            for i in range(len(FEATURES_ORDER))
        }
        top = sorted(contribs.items(), key=lambda x: abs(x[1]), reverse=True)[:max_feats]
        return dict(top)
    except Exception as e:
        print("SHAP error", e)
        return {}