import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import pandas as pd
from pipeline.simulator import simulate_flights, simulate_traffic_scenario
from pipeline.config import AIRPORT

def test_simulate_flights_returns_dataframe():
    df = simulate_flights(n_flights=5)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5

def test_required_columns_present():
    df = simulate_flights(n_flights=5)
    required = ["flight_id", "callsign", "aircraft_type", "category",
                "wake_class", "lat", "lon", "altitude_ft", "speed_kt",
                "heading_deg", "vertical_rate", "squawk", "priority", "eta_min"]
    for col in required:
        assert col in df.columns, f"Colonne manquante: {col}"

def test_positions_inside_tma():
    df = simulate_flights(n_flights=20)
    airport_lat = AIRPORT["lat"]
    airport_lon = AIRPORT["lon"]
    for _, row in df.iterrows():
        dlat = abs(airport_lat - row["lat"]) * 60
        dlon = abs(airport_lon - row["lon"]) * 60
        distance_nm = (dlat**2 + dlon**2) ** 0.5
        assert distance_nm <= 55, f"Vol hors TMA: {distance_nm:.1f} NM"

def test_eta_positive():
    df = simulate_flights(n_flights=10)
    assert (df["eta_min"] > 0).all()

def test_scenarios():
    for scenario in ["normal", "dense", "emergency"]:
        df = simulate_traffic_scenario(scenario)
        assert len(df) > 0, f"Scénario {scenario} vide"

def test_priority_values_valid():
    df = simulate_flights(n_flights=30, include_emergency=True)
    valid = {"NORMAL", "FUEL_CRITICAL", "EMERGENCY", "RADIO_FAIL", "MEDICAL"}
    assert set(df["priority"].unique()).issubset(valid)

def test_sorted_by_eta():
    df = simulate_flights(n_flights=10)
    assert list(df["eta_min"]) == sorted(df["eta_min"].tolist())

def test_wake_class_valid():
    df = simulate_flights(n_flights=20)
    valid = {"LIGHT", "MEDIUM", "HEAVY", "SUPER"}
    assert set(df["wake_class"].unique()).issubset(valid)

def test_altitude_range():
    df = simulate_flights(n_flights=20)
    assert (df["altitude_ft"] >= 3000).all()
    assert (df["altitude_ft"] <= 15000).all()