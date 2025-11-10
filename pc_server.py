from fastapi import FastAPI
from pydantic import BaseModel
import random
from fastapi.responses import FileResponse
import os


app = FastAPI()

class SensorData(BaseModel):
    imu: dict
    counts: dict

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/download-data")
def download_data():
    file_path = "wheelz_data.csv"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="wheelz_data.csv", media_type="text/csv")
    else:
        return {"error": "No data file found"}

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
    with open("robot_data.csv", "a") as f:
        f.write(f"{imu['gx']},{imu['gy']},{imu['gz']},{counts['left']},{counts['right']}\n")
    return {}
