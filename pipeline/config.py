AIRPORT = {
    "icao": "GLMM",
    "name": "Aéroport Hassan I Laâyoune",
    "lat": 27.1518,
    "lon": -13.4156,
    "elevation_ft": 207,
    "runway": {
        "heading_deg": 35,
        "length_m": 3100,
        "ils_frequency": 109.9,
        "glide_angle_deg": 3.0,
        "faf_distance_nm": 9.0,
    },
    "tma_radius_nm": 50,
    "transition_altitude_ft": 6000,
}

WAKE_SEPARATION_NM = {
    "SUPER":  {"SUPER": 3, "HEAVY": 6, "MEDIUM": 7, "LIGHT": 8},
    "HEAVY":  {"SUPER": 3, "HEAVY": 4, "MEDIUM": 5, "LIGHT": 6},
    "MEDIUM": {"SUPER": 3, "HEAVY": 3, "MEDIUM": 3, "LIGHT": 5},
    "LIGHT":  {"SUPER": 3, "HEAVY": 3, "MEDIUM": 3, "LIGHT": 3},
}

AIRCRAFT_CATEGORIES = {
    "A": {"vat_max": 90,  "wake": "LIGHT"},
    "B": {"vat_max": 120, "wake": "LIGHT"},
    "C": {"vat_max": 140, "wake": "MEDIUM"},
    "D": {"vat_max": 165, "wake": "HEAVY"},
    "E": {"vat_max": 210, "wake": "HEAVY"},
    "F": {"vat_max": 999, "wake": "SUPER"},
}

AIRCRAFT_FLEET = [
    {"type": "ATR72", "category": "B", "wake": "LIGHT",  "typical_speed_kt": 248},
    {"type": "B737",  "category": "C", "wake": "MEDIUM", "typical_speed_kt": 450},
    {"type": "A320",  "category": "C", "wake": "MEDIUM", "typical_speed_kt": 450},
    {"type": "A321",  "category": "C", "wake": "MEDIUM", "typical_speed_kt": 450},
    {"type": "B738",  "category": "C", "wake": "MEDIUM", "typical_speed_kt": 450},
]

SQUAWK_PRIORITY = {
    "7700": "EMERGENCY",
    "7600": "RADIO_FAIL",
    "7500": "EMERGENCY",
}