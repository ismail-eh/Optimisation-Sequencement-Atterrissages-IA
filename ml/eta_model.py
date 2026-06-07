import os
import pickle
import numpy as np
import pandas as pd
import mlflow
import mlflow.sklearn
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
from ml.features import build_features
from pipeline.simulator import simulate_traffic_scenario

MODEL_PATH = "ml/models/eta_model.pkl"

def generate_training_data(n_scenarios=200):
    frames = []
    for _ in range(n_scenarios):
        import random
        scenario = random.choice(["normal", "dense", "emergency"])
        df = simulate_traffic_scenario(scenario)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

def train_eta_model():
    print("📦 Génération données d'entraînement...")
    df = generate_training_data(n_scenarios=200)

    X = build_features(df)
    y = df["eta_min"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("ETA_Prediction")
    with mlflow.start_run(run_name="XGBoost_ETA"):
        model = XGBRegressor(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.8,
            random_state=42,
            verbosity=0,
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        mae  = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 6)
        mlflow.log_metric("MAE", round(mae, 4))
        mlflow.log_metric("RMSE", round(rmse, 4))
        mlflow.sklearn.log_model(model, "eta_model")

        print(f"✅ ETA Model — MAE: {mae:.3f} min | RMSE: {rmse:.3f} min")

    os.makedirs("ml/models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Modèle sauvegardé → {MODEL_PATH}")
    return model

def load_eta_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict_eta(df: pd.DataFrame) -> pd.Series:
    model = load_eta_model()
    X = build_features(df)
    return pd.Series(model.predict(X), index=df.index, name="eta_predicted")