import random
import pandas as pd
import numpy as np
from pipeline.config import WAKE_SEPARATION_NM

SPEED_KT_AVG  = 400
NM_PER_MINUTE = SPEED_KT_AVG / 60

PRIORITY_ORDER = {
    "EMERGENCY":     0,
    "RADIO_FAIL":    1,
    "FUEL_CRITICAL": 2,
    "MEDICAL":       2,
    "NORMAL":        3,
}

def _schedule_sequence(flights: list) -> tuple:
    """Calcule ETAs schedulés + fitness pour une séquence donnée."""
    scheduled_etas = []
    last_eta  = 0
    last_wake = None
    total_wait = 0
    penalty    = 0

    for flight in flights:
        eta = flight.get("eta_predicted") or flight["eta_min"]
        if last_wake:
            sep_nm  = WAKE_SEPARATION_NM[last_wake][flight["wake_class"]]
            min_sep = sep_nm / NM_PER_MINUTE
            sched   = max(eta, last_eta + min_sep)
        else:
            sched = eta

        wait = max(0, sched - eta)
        priority_score = PRIORITY_ORDER.get(flight["priority"], 3)

        if priority_score == 0 and len(scheduled_etas) > 0:
            penalty += len(scheduled_etas) * 100

        total_wait    += wait
        scheduled_etas.append(sched)
        last_eta  = sched
        last_wake = flight["wake_class"]

    fitness = total_wait + penalty
    return fitness, scheduled_etas

def genetic_sequence(df: pd.DataFrame, generations=50, pop_size=30) -> pd.DataFrame:
    """
    Algorithme Génétique:
    - Population de séquences aléatoires
    - Sélection par fitness (minimise temps attente)
    - Croisement + mutation
    - Retourne meilleure séquence trouvée
    """
    flights = df.copy().to_dict("records")
    n       = len(flights)

    # Force urgences en premier
    emergency = [f for f in flights if PRIORITY_ORDER.get(f["priority"], 3) == 0]
    normal    = [f for f in flights if PRIORITY_ORDER.get(f["priority"], 3) > 0]

    def random_individual():
        ind = emergency.copy()
        rest = normal.copy()
        random.shuffle(rest)
        return ind + rest

    population = [random_individual() for _ in range(pop_size)]
    best_seq   = None
    best_fit   = float("inf")

    for _ in range(generations):
        scored = [(seq, _schedule_sequence(seq)[0]) for seq in population]
        scored.sort(key=lambda x: x[1])

        if scored[0][1] < best_fit:
            best_fit = scored[0][1]
            best_seq = scored[0][0]

        elite    = [s for s, _ in scored[:pop_size // 3]]
        children = []

        while len(children) < pop_size - len(elite):
            p1, p2 = random.sample(elite, 2)
            cut    = random.randint(1, n - 1)
            child  = p1[:cut] + [f for f in p2 if f not in p1[:cut]]

            if random.random() < 0.2 and len(normal) >= 2:
                i, j = random.sample(range(len(emergency), n), 2)
                child[i], child[j] = child[j], child[i]

            children.append(child)

        population = elite + children

    _, scheduled_etas = _schedule_sequence(best_seq)
    result = pd.DataFrame(best_seq).reset_index(drop=True)
    result["scheduled_eta"] = [round(e, 3) for e in scheduled_etas]
    result["sequence_pos"]  = result.index + 1
    result["algorithm"]     = "GENETIC"
    return result

def compute_metrics(sequenced: pd.DataFrame) -> dict:
    n          = len(sequenced)
    wait_times = []
    separations = []

    for i in range(n):
        wait_times.append(max(0, sequenced.iloc[i]["scheduled_eta"] - sequenced.iloc[i]["eta_min"]))

    for i in range(1, n):
        separations.append(sequenced.iloc[i]["scheduled_eta"] - sequenced.iloc[i-1]["scheduled_eta"])

    return {
        "algorithm":      "GENETIC",
        "n_flights":      n,
        "total_wait_min": round(sum(wait_times), 2),
        "avg_wait_min":   round(sum(wait_times) / n, 2),
        "max_wait_min":   round(max(wait_times), 2),
        "avg_separation": round(sum(separations) / len(separations), 2) if separations else 0,
        "min_separation": round(min(separations), 2) if separations else 0,
    }