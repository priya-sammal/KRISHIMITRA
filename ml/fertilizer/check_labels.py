import pickle

with open("crop_encoder.pkl", "rb") as f:
    crop_enc = pickle.load(f)

with open("soil_encoder.pkl", "rb") as f:
    soil_enc = pickle.load(f)

print("Crops:", list(crop_enc.classes_))
print("Soils:", list(soil_enc.classes_))

