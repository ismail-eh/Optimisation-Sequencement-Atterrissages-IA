import os
import pickle
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from ml.features import build_features, encode_priority
from pipeline.simulator import simulate_traffic_scenario

MODEL_PATH = "ml/models/priority_model.pkl"

PRIORITY_LABELS = {0: "NORMAL", 1: "FUEL_CRITICAL", 2: "RADIO_FAIL", 3: "EMERGENCY"}

def generate_training_data(n_scenarios=200):
    frames = []
    for _ in range(n_scenarios):
        import random
        scenario = random.choice(["normal", "dense", "emergency"])
        df = simulate_traffic_scenario(scenario)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

def train_priority_model():
    print("📦 Génération données d'entraînement...")
    df = generate_training_data(n_scenarios=200)

    X = build_features(df)
    y = df["priority"].apply(encode_priority)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    mlflow.set_experiment("Priority_Classification")
    with mlflow.start_run(run_name="RandomForest_Priority"):
        model = RandomForestClassifier(
            n_estimators=200,
            max_depth=8,
            random_state=42,
            class_weight="balanced",
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)

        mlflow.log_param("n_estimators", 200)
        mlflow.log_param("max_depth", 8)
        mlflow.log_metric("accuracy", round(acc, 4))
        mlflow.sklearn.log_model(model, "priority_model")

        print(f"✅ Priority Model — Accuracy: {acc:.3f}")
        labels_present = sorted(set(y_test) | set(y_pred))
        target_names = [PRIORITY_LABELS[l] for l in labels_present]
        print(classification_report(y_test, y_pred, labels=labels_present, target_names=target_names))


    os.makedirs("ml/models", exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"✅ Modèle sauvegardé → {MODEL_PATH}")
    return model

def load_priority_model():
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)

def predict_priority(df: pd.DataFrame) -> pd.Series:
    model = load_priority_model()
    X = build_features(df)
    preds = model.predict(X)
    return pd.Series([PRIORITY_LABELS[p] for p in preds], index=df.index, name="priority_predicted")