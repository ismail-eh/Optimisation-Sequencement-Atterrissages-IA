import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200

def test_get_flights_normal():
    r = client.get("/api/flights?scenario=normal")
    assert r.status_code == 200
    data = r.json()
    assert "flights" in data
    assert "count"   in data
    assert data["count"] > 0

def test_get_flights_dense():
    r = client.get("/api/flights?scenario=dense")
    assert r.status_code == 200
    assert r.json()["count"] >= 10

def test_get_flights_emergency():
    r = client.get("/api/flights?scenario=emergency")
    assert r.status_code == 200
    assert r.json()["count"] > 0

def test_flights_have_required_fields():
    r = client.get("/api/flights?scenario=normal")
    flight = r.json()["flights"][0]
    for field in ["flight_id", "callsign", "lat", "lon",
                  "altitude_ft", "speed_kt", "eta_min", "priority"]:
        assert field in flight, f"Champ manquant: {field}"

def test_sequence_greedy():
    r = client.get("/api/sequence?scenario=dense&algorithm=greedy")
    assert r.status_code == 200
    data = r.json()
    assert "sequence" in data
    assert "metrics"  in data
    assert len(data["sequence"]) > 0

def test_sequence_fcfs():
    r = client.get("/api/sequence?scenario=normal&algorithm=fcfs")
    assert r.status_code == 200
    assert len(r.json()["sequence"]) > 0

def test_sequence_genetic():
    r = client.get("/api/sequence?scenario=normal&algorithm=genetic")
    assert r.status_code == 200
    assert len(r.json()["sequence"]) > 0

def test_compare_algorithms():
    r = client.get("/api/compare?scenario=dense")
    assert r.status_code == 200
    data = r.json()
    assert "results" in data
    assert "fcfs"    in data["results"]
    assert "greedy"  in data["results"]
    assert "genetic" in data["results"]

def test_compare_has_metrics():
    r    = client.get("/api/compare?scenario=dense")
    data = r.json()
    for algo in ["fcfs", "greedy", "genetic"]:
        assert "metrics"  in data["results"][algo]
        assert "sequence" in data["results"][algo]

def test_metrics_values_positive():
    r       = client.get("/api/sequence?scenario=dense&algorithm=greedy")
    metrics = r.json()["metrics"]
    assert metrics["n_flights"]       > 0
    assert metrics["total_wait_min"]  >= 0
    assert metrics["avg_wait_min"]    >= 0