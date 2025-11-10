from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI()

class SensorData(BaseModel):
    imu: dict
    counts: dict

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/update")
def update(data: SensorData):
    """
    Called by the Flutter app every few seconds.
    Receives IMU + encoder data, returns an RL action.
    Replace the random policy below with your RL model.
    """
    imu = data.imu
    counts = data.counts

    # ---- RL Decision Logic (temporary placeholder) ----
    print(f"IMU: {imu}, COUNTS: {counts}, RL ACTION: none")
    return {}
