# 🛡️ How FraudShield AI Scores Transactions & Prevents Fraud
*(A Simple, Human-Friendly Guide)*

---

## 💡 The Core Idea in 30 Seconds

Imagine a smart digital security guard watching over every payment in real time. 

Whenever a transaction happens, FraudShield AI quickly checks 3 things:
1. **The Details**: Is this amount normal for this account? Is the merchant a high-risk category like crypto or gold?
2. **The Device & Network**: Is the payment coming from the usual phone? Is the money going to a known scammer account?
3. **The Behavior**: Is the typing rhythm normal? Are there 10 transactions happening in 2 minutes?

FraudShield AI calculates a single **Risk Score from 1 to 99**:

```text
 1 ────────────── 34 ────────────── 69 ────────────── 99
 │   🟢 APPROVE    │   🟡 STEP-UP MFA │   🔴 BLOCK    │
 │  Safe & Instant │   Ask for OTP    │ Decline & Stop│
```

---

## 🔍 The 3 Checks Performed on Every Payment

```
                        ┌──────────────────────────────┐
                        │   Incoming Payment Request   │
                        └──────────────┬───────────────┘
                                       │
     ┌─────────────────────────────────┼─────────────────────────────────┐
     │                                 │                                 │
     ▼                                 ▼                                 ▼
┌──────────────────────────┐ ┌──────────────────────────┐ ┌──────────────────────────┐
│  1. Money & Merchant     │ │  2. Device & Recipient   │ │  3. Behavior & Speed     │
│  • High amount vs balance│ │  • Known scammer account │ │  • Typing rhythm check   │
│  • Transfer vs payment   │ │  • Mule-ring network     │ │  • Rapid transaction count│
│  • Gold/crypto category  │ │  • New phone fingerprint │ │  • Unrecognized device   │
└────────────┬─────────────┘ └────────────┬─────────────┘ └────────────┬─────────────┘
             │                            │                            │
             └────────────────────────────┼────────────────────────────┘
                                          │
                                          ▼
                             ┌──────────────────────────┐
                             │  Calculate Risk Score    │
                             │        (1 to 99)         │
                             └────────────┬─────────────┘
                                          │
                   ┌──────────────────────┼──────────────────────┐
                   │                      │                      │
                   ▼                      ▼                      ▼
           🟢 Score 1 - 34        🟡 Score 35 - 69        🔴 Score 70 - 99
          ┌────────────────┐     ┌────────────────┐     ┌────────────────┐
          │    APPROVE     │     │  STEP-UP MFA   │     │     BLOCK      │
          │ Instant & Safe │     │ Ask for OTP    │     │ Decline Fraud  │
          └────────────────┘     └────────────────┘     └────────────────┘
```

---

## 🚦 How Decisions Are Made (Simple Rules)

### 🟢 1. APPROVE (Risk Score: 1 to 34)
* **What it means**: Everything looks normal, safe, and familiar.
* **Real-Life Example**: Paying ₹450 for groceries at your local store on your regular smartphone.
* **Action**: Payment completes instantly with zero delay.

---

### 🟡 2. STEP-UP MFA (Risk Score: 35 to 69)
* **What it means**: Something is slightly new or unusual, but not definitely fraud.
* **Real-Life Example**: Buying a ₹25,000 laptop from a new browser you haven't used before.
* **Action**: The system pauses and asks you to enter an **OTP / Fingerprint** to verify it's really you.

---

### 🔴 3. BLOCK (Risk Score: 70 to 99)
* **What it means**: High danger! Multiple red flags triggered at the same time.
* **Real-Life Example**: Sending ₹2,20,000 to a gold merchant from a brand-new device in another country, with 8 transactions in 5 minutes.
* **Action**: The payment is blocked instantly to protect your bank account, and an alert is sent to fraud investigators.

---

## 🧾 The SHAP Investigator Receipt Explained

Instead of an "AI black box" that gives no explanation, FraudShield AI generates an **Explainability Receipt** for every payment.

The receipt calculates simple **Points**:
* **🔴 Red Points (+15, +24)**: Suspicious signals that **increase** fraud risk.
* **🟢 Green Points (-8, -12)**: Normal signals that **lower** fraud risk.

### Example Receipt for a Blocked Fraud Attack:

```text
🧾 TXN-5001 · QuickGold Traders (₹2,20,000)

TRANSACTION PATTERN
+24 pts ── Amount is 12.5x the account balance
+10 pts ── High-risk merchant category (Gold / Gift Cards)

NETWORK GRAPH
+28 pts ── Recipient account linked to suspected mule ring

BEHAVIORAL SEQUENCE
+22 pts ── High velocity: 8 transactions in 5 minutes
+18 pts ── Typing rhythm deviates from owner profile

==================================================
COMPOSITE RISK SCORE: 99
DECISION: BLOCK · SENT TO INVESTIGATOR QUEUE
```

---

## 💡 Summary Table

| Risk Level | Score Range | What the AI Noticed | What Happens Next |
| :--- | :---: | :--- | :--- |
| **🟢 Low Risk** | **1 – 34** | Usual spending amount, trusted shop, familiar phone | **Approved instantly** |
| **🟡 Medium Risk** | **35 – 69** | Slightly larger amount or new device | **Asks for OTP / Fingerprint (2FA)** |
| **🔴 High Risk** | **70 – 99** | Huge balance drain, scam network link, bot-like typing speed | **Blocked immediately to protect money** |
