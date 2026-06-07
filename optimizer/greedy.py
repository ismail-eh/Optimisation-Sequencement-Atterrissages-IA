import pandas as pd
from pipeline.config import WAKE_SEPARATION_NM

SPEED_KT_AVG  = 400
NM_PER_MINUTE = SPEED_KT_AVG / 60

PRIORITY_ORDER = {
    "EMERGENCY":    0,
    "RADIO_FAIL":   1,
    "FUEL_CRITICAL": 2,
    "MEDICAL":      2,
    "NORMAL":       3,
}

def _min_separation_min(leader_wake: str, follower_wake: str) -> float:
    """Convertit séparation NM → minutes selon vitesse moyenne."""
    sep_nm = WAKE_SEPARATION_NM[leader_wake][follower_wake]
    return sep_nm / NM_PER_MINUTE

def greedy_sequence(df: pd.DataFrame) -> pd.DataFrame:
    """
    Algorithme Greedy:
    1. Priorité absolue aux urgences
    2. Respecte séparations ICAO wake turbulence
    3. Minimise temps d'attente global
    """
    flights    = df.copy().to_dict("records")
    sequenced  = []
    remaining  = sorted(flights, key=lambda x: (PRIORITY_ORDER.get(x["priority"], 3), x["eta_min"]))
    last_eta   = 0
    last_wake  = None

    while remaining:
        best       = None
        best_score = float("inf")
        best_eta   = 0

        for flight in remaining:
            eta = flight["eta_predicted"] if "eta_predicted" in flight and flight["eta_predicted"] else flight["eta_min"]

            if last_wake:
                min_sep = _min_separation_min(last_wake, flight["wake_class"])
                scheduled_eta = max(eta, last_eta + min_sep)
            else:
                scheduled_eta = eta

            priority_score = PRIORITY_ORDER.get(flight["priority"], 3)
            score = priority_score * 1000 + scheduled_eta

            if score < best_score:
                best_score = score
                best       = flight
                best_eta   = scheduled_eta

        best["scheduled_eta"] = round(best_eta, 3)
        best["algorithm"]     = "GREEDY"
        sequenced.append(best)
        remaining.remove(best)
        last_eta  = best_eta
        last_wake = best["wake_class"]

    result = pd.DataFrame(sequenced).reset_index(drop=True)
    result["sequence_pos"] = result.index + 1
    return result

def compute_metrics(sequenced: pd.DataFrame) -> dict:
    n = len(sequenced)
    wait_times   = []
    separations  = []

    for i in range(n):
        eta_orig  = sequenced.iloc[i]["eta_min"]
        eta_sched = sequenced.iloc[i]["scheduled_eta"]
        wait_times.append(max(0, eta_sched - eta_orig))

    for i in range(1, n):
        sep = sequenced.iloc[i]["scheduled_eta"] - sequenced.iloc[i-1]["scheduled_eta"]
        separations.append(sep)

    return {
        "algorithm":      "GREEDY",
        "n_flights":      n,
        "total_wait_min": round(sum(wait_times), 2),
        "avg_wait_min":   round(sum(wait_times) / n, 2),
        "max_wait_min":   round(max(wait_times), 2),
        "avg_separation": round(sum(separations) / len(separations), 2) if separations else 0,
        "min_separation": round(min(separations), 2) if separations else 0,
    }