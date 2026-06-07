import numpy as np
import pandas as pd
import uuid
import random
from datetime import datetime
from pipeline.config import AIRPORT, AIRCRAFT_FLEET, SQUAWK_PRIORITY

np.random.seed(42)

def _random_position_in_tma(center_lat, center_lon, min_nm=15, max_nm=45):
    angle = np.random.uniform(0, 360)
    distance_nm = np.random.uniform(min_nm, max_nm)
    distance_deg = distance_nm / 60.0
    lat = center_lat + distance_deg * np.cos(np.radians(angle))
    lon = center_lon + distance_deg * np.sin(np.radians(angle)) / np.cos(np.radians(center_lat))
    return round(lat, 6), round(lon, 6)

def _estimate_eta(lat, lon, speed_kt, airport_lat, airport_lon):
    dlat = airport_lat - lat
    dlon = airport_lon - lon
    distance_nm = np.sqrt((dlat * 60) ** 2 + (dlon * 60 * np.cos(np.radians(lat))) ** 2)
    return round((distance_nm / speed_kt) * 60, 2)

def _random_squawk(emergency_prob=0.05):
    if random.random() < emergency_prob:
        return random.choice(["7700", "7600"])
    return str(random.randint(1000, 7499)).zfill(4)

def simulate_flights(n_flights=5, include_emergency=True):
    airport_lat = AIRPORT["lat"]
    airport_lon = AIRPORT["lon"]
    records = []

    for _ in range(n_flights):
        aircraft = random.choice(AIRCRAFT_FLEET)
        lat, lon = _random_position_in_tma(airport_lat, airport_lon)
        speed_kt = aircraft["typical_speed_kt"] * np.random.uniform(0.85, 1.05)
        altitude_ft = np.random.uniform(3000, 15000)
        vertical_rate = np.random.uniform(-1800, -600)
        eta_min = _estimate_eta(lat, lon, speed_kt, airport_lat, airport_lon)
        squawk = _random_squawk(emergency_prob=0.05 if include_emergency else 0)

        priority = SQUAWK_PRIORITY.get(squawk, "NORMAL")
        if priority == "NORMAL" and np.random.random() < 0.1:
            priority = "FUEL_CRITICAL"

        records.append({
            "flight_id":     str(uuid.uuid4())[:8].upper(),
            "callsign":      f"RAM{random.randint(100, 999)}",
            "aircraft_type": aircraft["type"],
            "category":      aircraft["category"],
            "wake_class":    aircraft["wake"],
            "lat":           lat,
            "lon":           lon,
            "altitude_ft":   round(altitude_ft, 0),
            "speed_kt":      round(speed_kt, 1),
            "heading_deg":   round(np.random.uniform(0, 360), 1),
            "vertical_rate": round(vertical_rate, 0),
            "squawk":        squawk,
            "priority":      priority,
            "eta_min":       eta_min,
            "timestamp":     datetime.utcnow().isoformat(),
        })

    return pd.DataFrame(records).sort_values("eta_min").reset_index(drop=True)

def simulate_traffic_scenario(scenario="normal"):
    scenarios = {
        "normal":    {"n": 5, "emergency": False},
        "dense":     {"n": 5, "emergency": False},
        "emergency": {"n": 5, "emergency": True},
    }
    cfg = scenarios.get(scenario, scenarios["normal"])
    return simulate_flights(n_flights=cfg["n"], include_emergency=cfg["emergency"])