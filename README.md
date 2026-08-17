# 🛡️ FraudShield AI — Real-Time Fraud Prevention & Explainable Risk Scoring

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Framework-009688.svg)](https://fastapi.tiangolo.com/)
[![XGBoost](https://img.shields.io/badge/XGBoost-Machine%20Learning-orange.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/license-MIT-purple.svg)](LICENSE)

**FraudShield AI** is an intelligent fraud detection system that protects bank accounts in real time. Whenever a payment is made, FraudShield AI analyzes the transaction in **under 0.05 seconds** and decides whether to **Approve**, ask for **OTP Verification (MFA)**, or **Block** the transaction to prevent theft.

Unlike "black box" AI tools, FraudShield AI generates a **simple digital receipt** for every transaction, explaining exactly *why* a payment was flagged or approved.

> 📖 **Guides & Specifications**:
> - [Hackathon Project Presentation Document](PROJECT_PRESENTATION_DOC.md) — Comprehensive guide written for judges & reviewers.
> - [Scoring System Guide](SCORING_SYSTEM.md) — Simple step-by-step guide to scoring rules and decisions.

---

## 🌟 Key Features

- ⚡ **Instant Payment Check**: Scores transactions in under 50 milliseconds without slowing down payments.
- 🧠 **3-Way Security Check**:
  - 📊 **Money & Merchant**: Checks if the amount is unusually high for the account or going to a risky shop (Crypto, Gold, Gift Cards).
  - 🌐 **Network Check**: Detects if the money is being sent to a known scammer account.
  - ⏱️ **Behavior & Typing Check**: Measures typing rhythm and detects if someone is triggering multiple rapid transactions.
- 🧾 **Simple Point Receipts**: Shows red points for suspicious signals and green points for trusted signals.
- 📡 **Live Stream Engine**: Streams transactions live using Server-Sent Events (SSE) from the backend.
- 🎨 **Visual Dashboard**: Dark-mode dashboard with live risk graphs, status filters, and row highlights.
- 🧪 **Interactive Test Simulator**: Test custom payments directly from the UI to see how FraudShield AI reacts.

---

## 📁 Repository Structure

```text
hackathon Adobe/
├── main.py                     # Backend API server & streaming engine
├── model_pipeline.py           # Machine learning model & SHAP receipt generator
├── index.html                  # Main live dashboard & simulator UI
├── fraudshield_ai_prototype.html # Standalone prototype dashboard
├── test_backend.py             # Automated test suite
├── PROJECT_PRESENTATION_DOC.md # Comprehensive hackathon presentation document for judges
├── SCORING_SYSTEM.md           # Simple guide to scoring rules & decisions
├── dataset.csv                 # Sample transaction dataset
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

---

## 🚀 Quick Start Guide

### Prerequisites

- Python **3.10** or higher installed.

### 1. Setup Virtual Environment

```bash
# Open project directory
cd "hackathon Adobe"

# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.\.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Start the Application

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

Open your browser and visit: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🔌 Simple API Overview

### 1. Score a Payment
- **URL**: `POST /api/score`
- **Request Payload**:
  ```json
  {
    "amount": 95000.0,
    "oldbalanceOrg": 10000.0,
    "channel": "Mobile app transfer",
    "merch_name": "QuickGold Traders",
    "merch_category": "Gift cards / gold",
    "is_high_risk": true,
    "mule_ring_flag": true,
    "is_new_device": true,
    "velocity_5m": 6,
    "biometric_sigma": 3.4
  }
  ```
- **Response**:
  ```json
  {
    "id": "TXN-3827",
    "time": "18:10:10",
    "amount": 95000.0,
    "score": 99,
    "decision": "block",
    "factors": [
      { "g": "tabular", "label": "Amount is 9.5x account balance", "pts": 24 },
      { "g": "graph", "label": "Recipient account linked to scam network", "pts": 28 },
      { "g": "sequence", "label": "Session velocity: 6 transactions in 5 minutes", "pts": 18 }
    ],
    "latency": 42
  }
  ```

### 2. Live Stream
- **URL**: `GET /api/stream`
- **Description**: Connects to the real-time stream of incoming scored transactions.

### 3. Summary Statistics
- **URL**: `GET /api/stats`
- **Response**:
  ```json
  {
    "approved": 290,
    "review": 0,
    "blocked": 61
  }
  ```

---

## 🧪 Automated Tests

Run tests to verify that the scoring pipeline and backend server are working properly:

```bash
pytest test_backend.py
```

Output:
```text
================ test session starts ================
collected 5 items

test_backend.py .....                         [100%]

================ 5 passed in 1.95s ==================
```

---

## 🛡️ License

Distributed under the MIT License.
