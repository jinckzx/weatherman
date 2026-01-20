from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import pandas as pd
from model_loader import MODELS

app = FastAPI(title="Weather Predictor API")

# ---------------------------
# Request schema
# ---------------------------
class WeatherRequest(BaseModel):
    type: str = Field(..., example="temperature")
    city: str = Field(..., example="delhi")
    timestamp: str = Field(..., example="2026-08-15 14:00")

# ---------------------------
# Prediction endpoint
# ---------------------------
@app.post("/weatherpredictor")
def weather_predictor(req: WeatherRequest):

    key = (req.type.lower(), req.city.lower())

    if key not in MODELS:
        raise HTTPException(
            status_code=400,
            detail="Invalid type or city. Use temperature/humidity and delhi/kolkata."
        )

    try:
        ds = pd.to_datetime(req.timestamp)
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format. Use YYYY-MM-DD HH:MM"
        )

    model = MODELS[key]

    df = pd.DataFrame({"ds": [ds]})
    forecast = model.predict(df)

    return {
        "city": req.city.lower(),
        "type": req.type.lower(),
        "timestamp": req.timestamp,
        "prediction": round(float(forecast.loc[0, "yhat"]), 2),
        "lower_bound": round(float(forecast.loc[0, "yhat_lower"]), 2),
        "upper_bound": round(float(forecast.loc[0, "yhat_upper"]), 2),
    }
