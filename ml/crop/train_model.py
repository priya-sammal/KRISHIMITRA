import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("../../DataSets/Crop_recommendation.csv")

# Features and label
X = df.drop("label", axis=1)
y = df["label"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model
model = RandomForestClassifier(n_estimators=200, random_state=42)
model.fit(X_train, y_train)

# Accuracy
print("Training complete. Accuracy:", model.score(X_test, y_test))

# Save model
with open("crop_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model saved as crop_model.pkl")
