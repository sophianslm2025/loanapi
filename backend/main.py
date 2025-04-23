# backend/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models import ClientFeatures, PredictionResponse
from serve_model import load_pipeline, predict_proba, explain_prediction

app = FastAPI(title="Eligibility‑Score API", version="1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # autorise les appels Streamlit
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = load_pipeline()

@app.post("/predict", response_model=PredictionResponse)
async def predict(client: ClientFeatures):
    try:
        score = predict_proba(pipeline, client.features)
        explanation = explain_prediction(pipeline, client.features)
        return {"score": score, "explanation": explanation}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# endpoint pour renvoyer un client exemple (facultatif)
@app.get("/sample/{client_id}")
async def sample(client_id: int):
    # À implémenter : récupérer dans la base ou CSV
    return {}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)