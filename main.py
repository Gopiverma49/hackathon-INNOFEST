import asyncio
import json
import random
import time
from typing import Optional
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, StreamingResponse
from pydantic import BaseModel

from model_pipeline import FraudShieldPipeline

app = FastAPI(
    title="FraudShield AI Backend Engine",
    description="Real-time Financial Fraud Detection & SHAP Explainability Engine",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = FraudShieldPipeline()

stats = {
    "total_scored": 0,
    "approved": 0,
    "review": 0,
    "blocked": 0,
    "latencies": []
}

txn_counter = 5000

merchants = [
    {"name": "Zomato", "cat": "Food delivery", "risk": 0},
    {"name": "Amazon Pay", "cat": "Marketplace", "risk": 0},
    {"name": "IRCTC", "cat": "Travel", "risk": 0},
    {"name": "Swiggy Instamart", "cat": "Grocery", "risk": 0},
    {"name": "Local Kirana (UPI)", "cat": "P2M UPI", "risk": 0},
    {"name": "Flipkart", "cat": "Marketplace", "risk": 0},
    {"name": "Uber", "cat": "Transport", "risk": 0},
    {"name": "New Payee — 98xxx4471", "cat": "P2P UPI", "risk": 1},
    {"name": "QuickGold Traders", "cat": "Gift cards / gold", "risk": 1},
    {"name": "CoinNova Exchange", "cat": "Crypto", "risk": 1},
    {"name": "ForexDirect", "cat": "Foreign exchange", "risk": 1},
    {"name": "ElectroMax Wholesale", "cat": "Electronics", "risk": 1}
]
high_risk_merchants = [m for m in merchants if m["risk"] == 1]

channels = ["UPI", "Card · Web checkout", "Card · POS", "Mobile app transfer"]
cities = ["Bengaluru, IN (home)", "Mumbai, IN (280 km away)", "Chennai, IN (350 km away)"]
far_cities = ["Lagos, NG (7,840 km away)", "Manila, PH (3,540 km away)", "Kyiv, UA (6,200 km away)", "Unknown VPN exit node"]

# Cache dashboard HTML template in memory
HTML_CACHE = ""
try:
    with open("index.html", "r", encoding="utf-8") as f:
        HTML_CACHE = f.read()
except Exception:
    pass

class TransactionPayload(BaseModel):
    amount: float
    oldbalanceOrg: Optional[float] = 10000.0
    oldbalanceDest: Optional[float] = 0.0
    newbalanceDest: Optional[float] = 0.0
    channel: Optional[str] = "UPI"
    merch_name: Optional[str] = "QuickPay"
    merch_category: Optional[str] = "General"
    is_high_risk: Optional[bool] = False
    velocity_5m: Optional[int] = 1
    biometric_sigma: Optional[float] = 0.5
    mule_ring_flag: Optional[bool] = False
    is_new_device: Optional[bool] = False
    geo_location: Optional[str] = "Bengaluru, IN"

def _record_and_format_txn(txn_id: str, amount: float, merch_name: str, merch_cat: str, channel: str, geo: str, is_new_dev: bool, res: dict) -> dict:
    """Unified helper function to record stats and format transaction responses."""
    global stats
    stats["total_scored"] += 1
    d = res["decision"]
    if d == "safe":
        stats["approved"] += 1
    elif d == "review":
        stats["review"] += 1
    else:
        stats["blocked"] += 1

    stats["latencies"].append(res["latency_ms"])
    if len(stats["latencies"]) > 200:
        stats["latencies"].pop(0)

    return {
        "id": txn_id,
        "time": time.strftime("%H:%M:%S"),
        "amount": amount,
        "merch": {"name": merch_name, "cat": merch_cat},
        "channel": channel,
        "geo": geo,
        "device": "New unrecognized device" if is_new_dev else "Known device",
        "score": res["score"],
        "decision": res["decision"],
        "factors": res["factors"],
        "groups": res["groups"],
        "latency": res["latency_ms"]
    }

@app.get("/", response_class=HTMLResponse)
def read_root():
    if HTML_CACHE:
        return HTML_CACHE
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return HTMLResponse(f"<h1>FraudShield AI API</h1><p>Dashboard missing: {e}</p>")

@app.post("/api/score")
def score_transaction(payload: TransactionPayload):
    res = pipeline.predict_and_explain(payload.model_dump())
    txn_id = f"TXN-{random.randint(1000, 9999)}"
    return _record_and_format_txn(
        txn_id=txn_id,
        amount=payload.amount,
        merch_name=payload.merch_name,
        merch_cat=payload.merch_category,
        channel=payload.channel,
        geo=payload.geo_location,
        is_new_dev=payload.is_new_device,
        res=res
    )

@app.get("/api/stats")
def get_stats():
    avg_lat = round(sum(stats["latencies"]) / len(stats["latencies"]), 1) if stats["latencies"] else 42.0
    return {
        "total_scored": stats["total_scored"],
        "approved": stats["approved"],
        "review": stats["review"],
        "blocked": stats["blocked"],
        "avg_latency_ms": avg_lat
    }

def generate_random_txn(fraud_rate: float = 15.0) -> dict:
    global txn_counter
    txn_counter += 1
    rate_threshold = fraud_rate / 100.0 if fraud_rate > 1.0 else fraud_rate
    is_fraud = random.random() < rate_threshold

    if is_fraud:
        merch = random.choice(high_risk_merchants)
        amount = round(random.uniform(4000, 220000), 2)
        geo = random.choice(far_cities)
        is_new_dev = True
        velocity = random.randint(4, 9)
        biometric = round(random.uniform(2.2, 4.5), 2)
        mule = random.random() < 0.75
        high_risk = True
        old_org = round(random.uniform(500, 15000), 2)
    else:
        merch = random.choice(merchants)
        amount = round(random.uniform(80, 18000), 2)
        geo = random.choice(cities)
        is_new_dev = random.random() < 0.1
        velocity = random.randint(1, 3)
        biometric = round(random.uniform(0.1, 1.2), 2)
        mule = False
        high_risk = merch["risk"] == 1
        old_org = round(random.uniform(20000, 150000), 2)

    channel = random.choice(channels)
    txn_dict = {
        "amount": amount,
        "oldbalanceOrg": old_org,
        "channel": channel,
        "merch_category": merch["cat"],
        "is_high_risk": high_risk,
        "velocity_5m": velocity,
        "biometric_sigma": biometric,
        "mule_ring_flag": mule,
        "is_new_device": is_new_dev,
        "geo_location": geo
    }

    res = pipeline.predict_and_explain(txn_dict)
    return _record_and_format_txn(
        txn_id=f"TXN-{txn_counter}",
        amount=amount,
        merch_name=merch["name"],
        merch_cat=merch["cat"],
        channel=channel,
        geo=geo,
        is_new_dev=is_new_dev,
        res=res
    )

@app.get("/api/stream")
async def stream_transactions(request: Request, rate: float = 15.0):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            txn_data = generate_random_txn(fraud_rate=rate)
            yield f"data: {json.dumps(txn_data)}\n\n"
            await asyncio.sleep(random.uniform(0.8, 1.6))

    return StreamingResponse(event_generator(), media_type="text/event-stream")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
