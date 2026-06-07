from fastapi import APIRouter, Query
from pipeline.simulator import simulate_traffic_scenario
from ml.eta_model import train_eta_model, predict_eta
from ml.priority_model import train_priority_model, predict_priority
from optimizer.fcfs import fcfs_sequence, compute_metrics as fcfs_metrics
from optimizer.greedy import greedy_sequence, compute_metrics as greedy_metrics
from optimizer.genetic import genetic_sequence, compute_metrics as genetic_metrics
import pandas as pd
import os

router = APIRouter(prefix="/api")

ETA_MODEL_PATH      = "ml/models/eta_model.pkl"
PRIORITY_MODEL_PATH = "ml/models/priority_model.pkl"

def ensure_models():
    if not os.path.exists(ETA_MODEL_PATH) or not os.path.exists(PRIORITY_MODEL_PATH):
        print("⚠️ Models na9sin — training automatique...")
        train_eta_model()
        train_priority_model()

def df_to_json(df: pd.DataFrame) -> list:
    return df.where(pd.notnull(df), None).to_dict(orient="records")

def get_enriched_df(scenario: str) -> pd.DataFrame:
    ensure_models()
    df = simulate_traffic_scenario(scenario)
    df["eta_predicted"]      = predict_eta(df)
    df["priority_predicted"] = predict_priority(df)
    return df

@router.get("/flights")
def get_flights(scenario: str = Query(default="normal")):
    df = get_enriched_df(scenario)
    return {"flights": df_to_json(df), "count": len(df)}

@router.get("/sequence")
def get_sequence(scenario: str = Query(default="normal"), algorithm: str = Query(default="greedy")):
    df = get_enriched_df(scenario)

    if algorithm == "fcfs":
        sequenced = fcfs_sequence(df)
        metrics   = fcfs_metrics(sequenced)
    elif algorithm == "genetic":
        sequenced = genetic_sequence(df)
        metrics   = genetic_metrics(sequenced)
    else:
        sequenced = greedy_sequence(df)
        metrics   = greedy_metrics(sequenced)

    return {"sequence": df_to_json(sequenced), "metrics": metrics}

@router.get("/compare")
def compare_algorithms(scenario: str = Query(default="dense")):
    df = get_enriched_df(scenario)

    fcfs    = fcfs_sequence(df)
    greedy  = greedy_sequence(df)
    genetic = genetic_sequence(df)

    return {
        "scenario": scenario,
        "results": {
            "fcfs":    {"sequence": df_to_json(fcfs),    "metrics": fcfs_metrics(fcfs)},
            "greedy":  {"sequence": df_to_json(greedy),  "metrics": greedy_metrics(greedy)},
            "genetic": {"sequence": df_to_json(genetic), "metrics": genetic_metrics(genetic)},
        }
    }

@router.get("/health")
def health():
    return {"status": "ok"}