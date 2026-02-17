from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os
import time
from typing import Optional

app = FastAPI()

# ---------- Data model ----------
class SensorData(BaseModel):
    imu: dict
    counts: dict
    action: str          # action currently being applied
    mode: str            # "manual" or "auto"


# Track previous encoder counts for deltas
last_left = None
last_right = None


# ---------- Root ----------
@app.get("/")
def root():
    return {"status": "ok"}


# ---------- Update endpoint ----------
@app.post("/update")
def update(data: SensorData):

    global last_left, last_right

    imu = data.imu
    counts = data.counts
    action = data.action
    mode = data.mode

    file_path = "wheelz_data.csv"

    # Ensure CSV exists
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("timestamp,gx,gy,gz,left,right,dLeft,dRight,speed,turn,action,mode\n")

    # ----- Encoder deltas -----
    left = counts['left']
    right = counts['right']

    if last_left is None:
        dLeft = 0
        dRight = 0
    else:
        dLeft = left - last_left
        dRight = right - last_right

    last_left = left
    last_right = right

    speed = (dLeft + dRight) / 2.0
    turn = (dRight - dLeft)

    timestamp = time.time()

    # Log row
    with open(file_path, "a") as f:
        f.write(f"{timestamp},{imu['gx']},{imu['gy']},{imu['gz']},{left},{right},{dLeft},{dRight},{speed},{turn},{action},{mode}\n")

    print(f"MODE: {mode} | ACTION: {action} | SPEED: {speed} | TURN: {turn}")

    # ----- Placeholder RL policy -----
    predicted_action = None

    if mode == "auto":
        # Later replace this with your trained model
        predicted_action = "stop"

        return {"action": predicted_action}

    # Manual mode returns nothing
    return {}
    

# ---------- Download endpoint ----------
@app.get("/download-data")
def download_data():
    file_path = "wheelz_data.csv"
    if os.path.exists(file_path):
        return FileResponse(path=file_path, filename="wheelz_data.csv", media_type="text/csv")
    else:
        return {"error": "No data file found"}
