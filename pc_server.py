from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    imu: dict
    counts: dict

@app.get("/")
def root():
    return {"status": "ok"}

@app.post("/update")
def update(data: SensorData):
    # RL / object-detection logic will go here later
    imu = data.imu
    counts = data.counts
    print("IMU:", imu, "COUNTS:", counts)
    # Example rule
    action = "forward"
    if abs(imu.get("gx", 0)) > 200:
        action = "left"
    return {"action": action}