import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import os

# -------------------------
# TRAIN MODEL
# -------------------------
def train_model(df):
    """
    Train a Random Forest model to predict failure
    """

    # Check required columns
    required_cols = ["temperature", "vibration", "pressure", "failure"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Missing column: {col}")

    # Features and target
    X = df[["temperature", "vibration", "pressure"]]
    y = df["failure"]

    # Handle small dataset case
    if len(df) < 10:
        raise ValueError("⚠️ Dataset too small to train model")

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Evaluation
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # Create models folder if not exists
    os.makedirs("models", exist_ok=True)

    # Save model
    joblib.dump(model, "models/failure_model.pkl")

    return acc


# -------------------------
# LOAD MODEL
# -------------------------
def load_model():
    """
    Load trained model from disk
    """

    model_path = "models/failure_model.pkl"

    if not os.path.exists(model_path):
        raise FileNotFoundError("⚠️ Model not found. Train it first.")

    return joblib.load(model_path)


# -------------------------
# PREDICT FAILURE
# -------------------------
def predict_failure(model, df):
    """
    Predict failure (0 or 1) for given data
    """

    required_cols = ["temperature", "vibration", "pressure"]

    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"❌ Missing column: {col}")

    X = df[required_cols]

    predictions = model.predict(X)

    return predictions


# -------------------------
# OPTIONAL: MODEL INFO
# -------------------------
def model_info(model):
    """
    Returns feature importance
    """

    features = ["temperature", "vibration", "pressure"]

    importance = model.feature_importances_

    info = dict(zip(features, importance))

    return info