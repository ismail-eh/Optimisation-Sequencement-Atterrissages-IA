import asyncio
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pipeline.simulator import simulate_traffic_scenario
from ml.eta_model import predict_eta
from ml.priority_model import predict_priority
from optimizer.greedy import greedy_sequence, compute_metrics
import pandas as pd

ws_router = APIRouter()

def build_update(scenario="dense") -> dict:
    df = simulate_traffic_scenario(scenario)
    df["eta_predicted"]      = predict_eta(df)
    df["priority_predicted"] = predict_priority(df)
    sequenced = greedy_sequence(df)
    metrics   = compute_metrics(sequenced)

    return {
        "flights":  df.where(pd.notnull(df), None).to_dict(orient="records"),
        "sequence": sequenced.where(pd.notnull(sequenced), None).to_dict(orient="records"),
        "metrics":  metrics,
    }

@ws_router.websocket("/ws/live")
async def websocket_live(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = build_update(scenario="dense")
            await websocket.send_text(json.dumps(data))
            await asyncio.sleep(5)  # update kol 5 secondes
    except WebSocketDisconnect:
        pass