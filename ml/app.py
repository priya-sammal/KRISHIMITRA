from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

HERE = os.path.dirname(os.path.abspath(__file__))

FERT_MODEL_PATH = os.path.join(HERE, "fertilizer", "fertilizer_model.pkl")
CROP_ENCODER_PATH = os.path.join(HERE, "fertilizer", "crop_encoder.pkl")
SOIL_ENCODER_PATH = os.path.join(HERE, "fertilizer", "soil_encoder.pkl")
FERT_ENCODER_PATH = os.path.join(HERE, "fertilizer", "fertilizer_encoder.pkl")

with open(FERT_MODEL_PATH, "rb") as f:
    fert_model = pickle.load(f)

with open(CROP_ENCODER_PATH, "rb") as f:
    crop_enc = pickle.load(f)

with open(SOIL_ENCODER_PATH, "rb") as f:
    soil_enc = pickle.load(f)

with open(FERT_ENCODER_PATH, "rb") as f:
    fert_enc = pickle.load(f)

CROP_MODEL_PATH = os.path.join(HERE, "crop", "crop_model.pkl")
with open(CROP_MODEL_PATH, "rb") as f:
    crop_model = pickle.load(f)

# ---------------- CROP PREDICTION ----------------
@app.route("/predict_crop", methods=["POST"])
def predict_crop():
    data = request.get_json(force=True)
    required = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

    try:
        features = [float(data[k]) for k in required]
    except Exception:
        return jsonify({"error": "error in converting"}), 400

    features = np.array(features).reshape(1, -1)

    pred = crop_model.predict(features)[0]

    proba = None
    try:
        if hasattr(crop_model, "predict_proba"):
            probs = crop_model.predict_proba(features)[0]
            classes = crop_model.classes_
            ordered = sorted(zip(classes, probs), key=lambda x: x[1], reverse=True)[:3]
            proba = [{"crop": str(c), "prob": float(p)} for c, p in ordered]
    except:
        pass

    return jsonify({
        "crop": str(pred),
        "top": proba
    })

@app.route("/predict_fertilizer", methods=["POST"])
def predict_fertilizer():
    data = request.get_json(force=True)

    try:
        row = {
    "N": float(data["N"]),
    "P": float(data["P"]),
    "K": float(data["K"]),
    "pH": float(data["ph"]),
    "Rainfall": float(data["rainfall"]),
    "Temperature": float(data["temperature"]),
    "Crop_encoded": crop_enc.transform([data["crop"]])[0],
    "Soil_encoded": soil_enc.transform([data["soil"]])[0]
}

    except Exception as e:
        return jsonify({"error": "error in converting inputs"}), 400

    df = pd.DataFrame([row])

    # Predict class
    pred_encoded = fert_model.predict(df)[0]
    fertilizer_name = fert_enc.inverse_transform([pred_encoded])[0]

    # Predict probabilities
    probs = fert_model.predict_proba(df)[0]
    classes = fert_model.classes_

    # Map class index -> fertilizer name
    fert_names = fert_enc.inverse_transform(classes)

    # Create list of (name, prob)
    ranked = sorted(
        zip(fert_names, probs),
        key=lambda x: x[1],
        reverse=True
    )

    top3 = [
        {"fertilizer": name, "confidence": round(float(prob) * 100, 2)}
        for name, prob in ranked[:3]
    ]

    best_confidence = top3[0]["confidence"]

    return jsonify({
        "fertilizer": fertilizer_name,
        "confidence": best_confidence,
        "top3": top3
    })


@app.route("/")
def home():
    return "Unified Crop + Fertilizer ML API running!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
