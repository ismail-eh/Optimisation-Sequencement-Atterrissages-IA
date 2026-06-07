import pandas as pd
from pipeline.config import WAKE_SEPARATION_NM

SPEED_KT_AVG  = 400
NM_PER_MINUTE = SPEED_KT_AVG / 60

def fcfs_sequence(df: pd.DataFrame) -> pd.DataFrame:
    sequenced  = df.copy().sort_values("eta_min").reset_index(drop=True)
    last_eta   = 0
    last_wake  = None
    scheduled  = []

    for _, row in sequenced.iterrows():
        eta = row["eta_predicted"] if "eta_predicted" in row and row["eta_predicted"] else row["eta_min"]
        if last_wake:
            sep_nm  = WAKE_SEPARATION_NM[last_wake][row["wake_class"]]
            min_sep = sep_nm / NM_PER_MINUTE
            sched   = max(eta, last_eta + min_sep)
        else:
            sched = eta
        scheduled.append(round(sched, 3))
        last_eta  = sched
        last_wake = row["wake_class"]

    sequenced["scheduled_eta"] = scheduled
    sequenced["sequence_pos"]  = sequenced.index + 1
    sequenced["algorithm"]     = "FCFS"
    return sequenced

def compute_metrics(sequenced: pd.DataFrame) -> dict:
    n           = len(sequenced)
    wait_times  = []
    separations = []

    for i in range(n):
        wait_times.append(max(0, sequenced.iloc[i]["scheduled_eta"] - sequenced.iloc[i]["eta_min"]))

    for i in range(1, n):
        separations.append(sequenced.iloc[i]["scheduled_eta"] - sequenced.iloc[i-1]["scheduled_eta"])

    return {
        "algorithm":      "FCFS",
        "n_flights":      n,
        "total_wait_min": round(sum(wait_times), 2),
        "avg_wait_min":   round(sum(wait_times) / n, 2),
        "max_wait_min":   round(max(wait_times), 2),
        "avg_separation": round(sum(separations) / len(separations), 2) if separations else 0,
        "min_separation": round(min(separations), 2) if separations else 0,
    }