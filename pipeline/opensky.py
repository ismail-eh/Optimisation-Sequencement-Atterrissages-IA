import requests
import pandas as pd
from datetime import datetime

OPENSKY_URL = "https://opensky-network.org/api/states/all"

def fetch_opensky(lat_min=25.0, lat_max=30.0, lon_min=-16.0, lon_max=-10.0):
    params = {"lamin": lat_min, "lomin": lon_min, "lamax": lat_max, "lomax": lon_max}
    try:
        resp = requests.get(OPENSKY_URL, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"⚠️ OpenSky indisponible: {e}")
        return None

    if not data.get("states"):
        print("⚠️ Aucun vol dans la zone")
        return None

    records = []
    for s in data["states"]:
        if s[5] is None or s[6] is None:
            continue
        records.append({
            "flight_id":     s[0],
            "callsign":      (s[1] or "").strip(),
            "lat":           s[6],
            "lon":           s[5],
            "altitude_ft":   round((s[7] or 0) * 3.28084, 0),
            "speed_kt":      round((s[9] or 0) * 1.94384, 1),
            "heading_deg":   s[10] or 0,
            "vertical_rate": round((s[11] or 0) * 196.85, 0),
            "squawk":        s[14] or "0000",
            "timestamp":     datetime.utcfromtimestamp(s[3]).isoformat(),
            "aircraft_type": "UNKNOWN",
            "category":      "C",
            "wake_class":    "MEDIUM",
            "priority":      "NORMAL",
            "eta_min":       None,
        })

    print(f"✅ {len(records)} vols récupérés depuis OpenSky")
    return pd.DataFrame(records)