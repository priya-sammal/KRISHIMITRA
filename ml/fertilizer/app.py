from flask import Flask, request, jsonify
import pickle
import numpy as np
import os
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

HERE = os.path.dirname(os.path.abspath(__file__))

# Load model and encoders
with open(os.path.join(HERE, "fertilizer_model.pkl"), "rb") as f:
    model = pickle.load(f)

with open(os.path.join(HERE, "crop_encoder.pkl"), "rb") as f:
    crop_enc = pickle.load(f)

with open(os.path.join(HERE, "soil_encoder.pkl"), "rb") as f:
    soil_enc = pickle.load(f)

with open(os.path.join(HERE, "fertilizer_encoder.pkl"), "rb") as f:
    fert_enc = pickle.load(f)


@app.route("/predict_fertilizer", methods=["POST"])
def predict_fertilizer():
    data = request.json

    try:
        nitrogen = float(data["nitrogen"])
        phosphorus = float(data["phosphorus"])
        potassium = float(data["potassium"])
        ph = float(data["ph"])
        rainfall = float(data["rainfall"])
        temperature = float(data["temperature"])
        crop = data["crop"]
        soil = data["soil"]

        # Encode crop & soil
        crop_encoded = crop_enc.transform([crop])[0]
        soil_encoded = soil_enc.transform([soil])[0]

        features = np.array([[nitrogen, phosphorus, potassium, ph, rainfall, temperature, crop_encoded, soil_encoded]])

        pred_encoded = model.predict(features)[0]
        fertilizer_name = fert_enc.inverse_transform([pred_encoded])[0]

        return jsonify({
            "success": True,
            "fertilizer": fertilizer_name
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
