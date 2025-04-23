from typing import Dict
from pydantic import BaseModel

class ClientFeatures(BaseModel):
    features: Dict[str, float]

class PredictionResponse(BaseModel):
    score: float  # probabilité d’octroi (0‑1)
    explanation: Dict[str, float]  # 3‑5 features principales (SHAP)