import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# Path to your CSV
DATA_PATH = os.path.join(HERE, "../../DataSets/Fertilizer_Prediction.csv")

df = pd.read_csv(DATA_PATH)

print("Columns:", df.columns)

# Encode categorical columns
crop_enc = LabelEncoder()
soil_enc = LabelEncoder()
fert_enc = LabelEncoder()

df["Crop_encoded"] = crop_enc.fit_transform(df["Crop"])
df["Soil_encoded"] = soil_enc.fit_transform(df["Soil"])
df["Fertilizer_encoded"] = fert_enc.fit_transform(df["Fertilizer"])

# Features (X) and target (y)
X = df[["N", "P", "K", "pH", "Rainfall", "Temperature", "Crop_encoded", "Soil_encoded"]]
y = df["Fertilizer_encoded"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

print("Fertilizer model training complete!")

# Save model + encoders
with open(os.path.join(HERE, "fertilizer_model.pkl"), "wb") as f:
    pickle.dump(model, f)

with open(os.path.join(HERE, "crop_encoder.pkl"), "wb") as f:
    pickle.dump(crop_enc, f)

with open(os.path.join(HERE, "soil_encoder.pkl"), "wb") as f:
    pickle.dump(soil_enc, f)

with open(os.path.join(HERE, "fertilizer_encoder.pkl"), "wb") as f:
    pickle.dump(fert_enc, f)

print(" Model and encoders saved!")
