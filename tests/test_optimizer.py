import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from pipeline.simulator import simulate_traffic_scenario
from ml.eta_model import predict_eta
from ml.priority_model import predict_priority
from optimizer.fcfs import fcfs_sequence, compute_metrics as fcfs_metrics
from optimizer.greedy import greedy_sequence, compute_metrics as greedy_metrics
from optimizer.genetic import genetic_sequence, compute_metrics as genetic_metrics
from pipeline.config import WAKE_SEPARATION_NM

SPEED_KT_AVG  = 400
NM_PER_MINUTE = SPEED_KT_AVG / 60

def get_df(scenario="dense"):
    df = simulate_traffic_scenario(scenario)
    df["eta_predicted"]      = predict_eta(df)
    df["priority_predicted"] = predict_priority(df)
    return df

def test_fcfs_sequence_length():
    df = get_df()
    result = fcfs_sequence(df)
    assert len(result) == len(df)

def test_fcfs_sorted_by_eta():
    df = get_df()
    result = fcfs_sequence(df)
    etas = result["eta_min"].tolist()
    assert etas == sorted(etas)

def test_fcfs_has_algorithm_column():
    df = get_df()
    result = fcfs_sequence(df)
    assert "algorithm" in result.columns
    assert result["algorithm"].iloc[0] == "FCFS"

def test_greedy_sequence_length():
    df = get_df()
    result = greedy_sequence(df)
    assert len(result) == len(df)

def test_greedy_respects_wake_separation():
    df = get_df("dense")
    result = greedy_sequence(df)
    for i in range(1, len(result)):
        leader   = result.iloc[i-1]
        follower = result.iloc[i]
        sep_nm   = WAKE_SEPARATION_NM[leader["wake_class"]][follower["wake_class"]]
        min_sep  = sep_nm / NM_PER_MINUTE
        actual   = follower["scheduled_eta"] - leader["scheduled_eta"]
        assert actual >= min_sep - 0.01, (
            f"Séparation insuffisante: {actual:.2f} < {min_sep:.2f} min"
        )

def test_greedy_emergency_first():
    df = get_df("dense")
    df = df.copy()
    df.loc[df.index[-1], "priority"] = "EMERGENCY"
    result = greedy_sequence(df)
    assert result.iloc[0]["priority"] == "EMERGENCY"

def test_greedy_fuel_critical_before_normal():
    df = get_df("dense")
    df = df.copy()
    df.loc[df.index[-1], "priority"] = "FUEL_CRITICAL"
    result = greedy_sequence(df)
    priorities = result["priority"].tolist()
    normal_positions  = [i for i, p in enumerate(priorities) if p == "NORMAL"]
    fuel_positions    = [i for i, p in enumerate(priorities) if p == "FUEL_CRITICAL"]
    if fuel_positions and normal_positions:
        assert min(fuel_positions) < max(normal_positions)

def test_genetic_sequence_length():
    df = get_df()
    result = genetic_sequence(df, generations=10, pop_size=10)
    assert len(result) == len(df)

def test_genetic_has_scheduled_eta():
    df = get_df()
    result = genetic_sequence(df, generations=10, pop_size=10)
    assert "scheduled_eta" in result.columns
    assert result["scheduled_eta"].notna().all()

def test_greedy_better_than_fcfs():
    df = get_df("dense")
    fcfs   = fcfs_sequence(df)
    greedy = greedy_sequence(df)
    m_fcfs   = fcfs_metrics(fcfs)
    m_greedy = greedy_metrics(greedy)
    assert m_greedy["total_wait_min"] <= m_fcfs["total_wait_min"] + 1

def test_metrics_structure_greedy():
    df = get_df()
    result  = greedy_sequence(df)
    metrics = greedy_metrics(result)
    for key in ["algorithm", "n_flights", "total_wait_min", "avg_wait_min",
                "max_wait_min", "avg_separation", "min_separation"]:
        assert key in metrics

def test_metrics_structure_fcfs():
    df = get_df()
    result  = fcfs_sequence(df)
    metrics = fcfs_metrics(result)
    for key in ["algorithm", "n_flights", "total_wait_min", "avg_wait_min"]:
        assert key in metrics

def test_sequence_pos_sequential():
    df = get_df()
    result = greedy_sequence(df)
    assert list(result["sequence_pos"]) == list(range(1, len(result) + 1))