import numpy as np
import pandas as pd
from pipeline.config import AIRPORT, AIRCRAFT_CATEGORIES

AIRPORT_LAT = AIRPORT["lat"]
AIRPORT_LON = AIRPORT["lon"]

def compute_distance_nm(lat, lon):
    dlat = AIRPORT_LAT - lat
    dlon = AIRPORT_LON - lon
    return np.sqrt((dlat * 60) ** 2 + (dlon * 60 * np.cos(np.radians(lat))) ** 2)

def compute_bearing(lat, lon):
    dlat = AIRPORT_LAT - lat
    dlon = AIRPORT_LON - lon
    angle = np.degrees(np.arctan2(dlon, dlat)) % 360
    return angle

def encode_category(category):
    mapping = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
    return mapping.get(category, 3)

def encode_wake(wake_class):
    mapping = {"LIGHT": 1, "MEDIUM": 2, "HEAVY": 3, "SUPER": 4}
    return mapping.get(wake_class, 2)

def encode_priority(priority):
    mapping = {
        "NORMAL": 0,
        "FUEL_CRITICAL": 1,
        "RADIO_FAIL": 2,
        "MEDICAL": 2,
        "EMERGENCY": 3,
    }
    return mapping.get(priority, 0)

def build_features(df: pd.DataFrame) -> pd.DataFrame:
    features = pd.DataFrame()
    features["distance_nm"]    = df.apply(lambda r: compute_distance_nm(r["lat"], r["lon"]), axis=1)
    features["bearing_deg"]    = df.apply(lambda r: compute_bearing(r["lat"], r["lon"]), axis=1)
    features["speed_kt"]       = df["speed_kt"]
    features["altitude_ft"]    = df["altitude_ft"]
    features["vertical_rate"]  = df["vertical_rate"]
    features["category_enc"]   = df["category"].apply(encode_category)
    features["wake_enc"]       = df["wake_class"].apply(encode_wake)
    features["priority_enc"]   = df["priority"].apply(encode_priority)
    features["descent_angle"]  = np.degrees(
        np.arctan2(-df["vertical_rate"] / 60, df["speed_kt"] * 1.852 / 60)
    ).clip(0, 15)
    return features