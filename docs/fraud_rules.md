# Fraud Detection Rules & Risk Engine

The risk scoring engine evaluates transaction events against heuristic rules in the Silver pipeline layer to identify suspicious activity and compute a composite risk score (0–100).

---

## 1. Risk Scoring & Banding

Every transaction is evaluated upon ingestion. Triggered rules contribute additive weights to compute the total `risk_score`:

* **LOW:** Score < 50
* **MEDIUM:** Score 50 to 74
* **HIGH:** Score >= 75

---

## 2. Rule Definitions

| Rule Code | Weight | Trigger Condition |
| :--- | :---: | :--- |
| `HIGH_AMOUNT` | 20 | Transaction amount >= $600 |
| `COUNTRY_MISMATCH` | 20 | IP or shipping country differs from billing country |
| `NEW_DEVICE_HIGH_AMOUNT` | 20 | First-time device ID used for a high transaction value |
| `HIGH_VELOCITY` | 15 | Customer transaction count spike in short window |
| `CARD_NOT_PRESENT_RISK` | 15 | Remote payment plus country mismatch |
| `MANY_CUSTOMERS_ON_DEVICE` | 10 | Multiple distinct customer IDs using a single device |
| `FAILED_LOGIN_BEFORE_PURCHASE` | 10 | Failed login activity recorded prior to transaction |

---
## 3. Pipeline Execution

The rule engine is executed during Silver layer processing inside `fraud_shield/pipeline/fraud/rules.py`:

```python
from fraud_shield.pipeline.fraud.rules import score_transactions

# Scores input transactions and appends risk_score, risk_band, and fraud_reason_codes
scored_df = score_transactions(transactions_df, logins_df, devices_df)