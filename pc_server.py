from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import time

app = FastAPI()

# ---------- Data model ----------
class SensorData(BaseModel):
    imu: dict
    counts: dict


# ---------- Root ----------
@app.get("/")
def root():
    return {"status": "ok"}


# ---------- Update endpoint ----------
@app.post("/update")
def update(data: SensorData):
    """
    Called by the Flutter app every few seconds.
    Receives IMU + encoder data, logs to CSV, and (optionally) returns an RL action.
    """

    imu = data.imu
    counts = data.counts

    # Ensure CSV exists and add header if needed
    file_path = "wheelz_data.csv"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("timestamp,gx,gy,gz,left,right,action\n")

    # ----- RL Decision Logic (placeholder) -----
    action = None  # <- change later to your model’s output

    # Log data
    timestamp = time.time()
    with open(file_path, "a") as f:
        f.write(f"{timestamp},{imu['gx']},{imu['gy']},{imu['gz']},{counts['left']},{counts['right']},{action}\n")

    # Print to console for debugging
    print(f"IMU: {imu}, COUNTS: {counts}, ACTION: {action}")

    # Return empty action (safe for data collection mode)
    return {}


# ---------- Download endpoint ----------
@app.get("/download-data")
def download_data():
    """
    Lets you download the collected CSV.
    """
    file_path = "wheelz_data.csv"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="wheelz_data.csv", media_type="text/csv")
    else:
        return {"error": "No data file found"}
