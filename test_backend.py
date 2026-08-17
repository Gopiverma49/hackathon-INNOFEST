import pytest
from fastapi.testclient import TestClient
from main import app
from model_pipeline import FraudShieldPipeline

client = TestClient(app)

def test_pipeline_clean_transaction():
    pipeline = FraudShieldPipeline()
    txn = {
        "amount": 450,
        "oldbalanceOrg": 25000,
        "channel": "UPI",
        "merch_category": "Grocery",
        "is_high_risk": False,
        "velocity_5m": 1,
        "biometric_sigma": 0.3,
        "mule_ring_flag": False,
        "is_new_device": False
    }
    res = pipeline.predict_and_explain(txn)
    assert "score" in res
    assert "decision" in res
    assert res["score"] < 45
    assert res["decision"] in ["safe", "review"]
    assert "factors" in res
    assert "groups" in res

def test_pipeline_fraud_transaction():
    pipeline = FraudShieldPipeline()
    txn = {
        "amount": 250000,
        "oldbalanceOrg": 15000,
        "channel": "Mobile app transfer",
        "merch_category": "Crypto",
        "is_high_risk": True,
        "velocity_5m": 8,
        "biometric_sigma": 3.8,
        "mule_ring_flag": True,
        "is_new_device": True
    }
    res = pipeline.predict_and_explain(txn)
    assert res["score"] >= 70
    assert res["decision"] == "block"
    assert len(res["factors"]) > 0

def test_fastapi_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "FraudShield" in response.text

def test_fastapi_stats_endpoint():
    response = client.get("/api/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_scored" in data
    assert "approved" in data
    assert "review" in data
    assert "blocked" in data

def test_fastapi_score_endpoint():
    payload = {
        "amount": 95000.0,
        "oldbalanceOrg": 10000.0,
        "channel": "Card · Web checkout",
        "merch_name": "QuickGold Traders",
        "merch_category": "Gift cards / gold",
        "is_high_risk": True,
        "mule_ring_flag": True,
        "is_new_device": True,
        "velocity_5m": 5,
        "biometric_sigma": 2.9,
        "geo_location": "Lagos, NG (7,840 km away)"
    }
    response = client.post("/api/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 95000.0
    assert "score" in data
    assert "decision" in data
    assert "factors" in data
