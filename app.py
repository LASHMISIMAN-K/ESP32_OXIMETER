import os, secrets
from datetime import datetime, timezone
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
DEVICE_TOKEN = os.environ.get("DEVICE_TOKEN", "").strip()

# Demo only: Vercel serverless instances do not share this in-memory state.
latest_data = {"heart_rate": None, "spo2": None, "updated_at": None}

@app.get("/")
def dashboard():
    return render_template("index.html")

@app.post("/api/data")
def receive_data():
    if DEVICE_TOKEN and not secrets.compare_digest(
        request.headers.get("X-Device-Token", ""), DEVICE_TOKEN
    ):
        return jsonify({"error": "Unauthorized device"}), 401
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Expected JSON"}), 400
    try:
        bpm, oxygen = float(data["heart_rate"]), float(data["spo2"])
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "heart_rate and spo2 must be numeric"}), 400
    if not (30 <= bpm <= 220 and 70 <= oxygen <= 100):
        return jsonify({"error": "Readings outside prototype range"}), 400
    latest_data.update(heart_rate=round(bpm, 1), spo2=round(oxygen, 1),
                       updated_at=datetime.now(timezone.utc).isoformat())
    return jsonify({"status": "ok"})

@app.get("/api/latest")
def get_latest():
    return jsonify(latest_data)

@app.get("/api/health")
def health():
    return jsonify({"status": "ok"})
