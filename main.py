import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="California Housing Price Prediction API",
    description="A simple API to predict house prices.",
    version="1.0.0"
)

# Locate and load the trained model
MODEL_PATH = os.path.join("models", "model.joblib")
if not os.path.exists(MODEL_PATH):
    MODEL_PATH = os.path.join("models", "housing_model.joblib")

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")


class HousingFeatures(BaseModel):
    longitude: float = -122.23
    latitude: float = 37.88
    housing_median_age: float = 41.0
    total_rooms: float = 880.0
    total_bedrooms: float = 129.0
    population: float = 322.0
    households: float = 126.0
    median_income: float = 8.3252
    ocean_proximity: str = "NEAR BAY"


@app.get("/")
def read_root():
    return {
        "message": "California Housing Price Prediction API is running",
        "status": "healthy"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict")
def predict(features: HousingFeatures):
    if model is None:
        raise HTTPException(status_code=500, detail="Model is not loaded")

    # Prepare DataFrame matching model input format
    data = features.model_dump() if hasattr(features, "model_dump") else features.dict()
    df = pd.DataFrame([data])

    try:
        prediction = model.predict(df)
        return {
            "predicted_house_value": round(float(prediction[0]), 2),
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
