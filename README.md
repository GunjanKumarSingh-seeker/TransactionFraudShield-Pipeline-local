# TransactionFraudShield Pipeline

**TransactionFraudShield Pipeline** is an end-to-end real-time fraud monitoring and data quality lakehouse engine. It ingests high-frequency transaction, login, and device telemetry streams, computes customer and device velocity features in real time, evaluates multi-factor heuristic risk scores, and surfaces operational alerts alongside automated data quality metrics.

---

## Executive Summary

Modern financial systems require continuous risk assessment and dataset validation. TransactionFraudShield addresses both by providing:
1. **Low-Latency Feature Engineering:** Computes stateful velocity counters and multi-entity aggregates across transaction and device events.
2. **Explainable Risk Scoring Engine:** Evaluates transactions across 7 weighted risk rules, outputting real-time risk scores ($0 - 100$), risk bands (`LOW`, `MEDIUM`, `HIGH`), and granular audit reason codes.
3. **Automated Data Quality Scorecards:** Evaluates incoming events against data contracts to flag missing payloads, invalid ranges, and schema violations before downstream consumption.
4. **Operational Monitoring & Dashboard:** Serves real-time KPI metrics, risk analytics, high-risk alert feeds, and customer profile aggregates.

---

## Architecture & Core Modules

* **`fraud_shield/`**: Core engine package containing data contract enforcement, telemetry transformations, and reporting modules.
* **`rules.py`**: Feature engineering and heuristic risk rule processing logic (`add_velocity_features`, `score_transactions`).
* **`transaction_simulator.py`**: High-throughput telemetry event stream generator for localized testing and live streaming.
* **`configs/`**: Configuration files for thresholds, risk weights, and topic mappings.
* **`data_contracts/`**: Schema definitions and data contract rules for incoming telemetry payloads.

---

## Fraud Rule Engine & Scoring Heuristics

Transactions are evaluated against 7 weighted rules. The final risk score is calculated as the sum of activated rule weights, capped at 100.

| Rule | Trigger Condition | Weight | Reason Code |
| :--- | :--- | :---: | :--- |
| **High Amount** | Transaction amount $\ge \$600$ | 20 | `HIGH_AMOUNT` |
| **Country Mismatch** | IP country $\neq$ billing country OR shipping country $\neq$ billing country | 20 | `COUNTRY_MISMATCH` |
| **New Device High Amount** | New device detected AND transaction amount $\ge \$600$ | 20 | `NEW_DEVICE_HIGH_AMOUNT` |
| **High Velocity** | Customer transaction count $\ge 4$ in window | 15 | `HIGH_VELOCITY` |
| **Card Not Present Risk** | Payment method is `card_not_present` AND country mismatch exists | 15 | `CARD_NOT_PRESENT_RISK` |
| **Device Sharing** | Device ID linked to $\ge 3$ distinct customer IDs | 10 | `MANY_CUSTOMERS_ON_DEVICE` |
| **Pre-Purchase Failed Logins** | $\ge 2$ failed login attempts prior to transaction | 10 | `FAILED_LOGIN_BEFORE_PURCHASE` |

### Classification Bands
* **LOW:** $0 - 39$
* **MEDIUM:** $40 - 69$
* **HIGH:** $70 - 100$

---

## Data Quality & Contract Enforcement

To prevent dirty data from corrupting downstream features and reporting, the pipeline evaluates incoming events against data quality contracts:

* **Schema Integrity Checks:** Verifies existence of required keys (`MISSING_EVENT_ID`, `MISSING_CUSTOMER_ID`, `MISSING_EVENT_TIMESTAMP`).
* **Domain Range Validation:** Flags anomalous field values (`NEGATIVE_AMOUNT`, `INVALID_IP_COUNTRY`).
* **Operational DQ Scorecard:** Computes pass rates and failure counts per topic in real time.

---

## Repository Structure

```text
TransactionFraudShield-Pipeline/
├── configs/                  # System and rule configurations
├── data_contracts/           # Data quality contract specifications
├── docs/                     # Architecture documentation & diagrams
├── fraud_shield/             # Core Python engine package
│   ├── pipeline/             # Data pipeline & feature processing
│   └── quality/              # Data contract validators
├── scripts/                  # Execution & operational startup scripts
├── tests/                    # Pytest suite for rules and feature engine
├── Makefile                  # Helper commands for local setup & execution
├── pyproject.toml            # Project dependencies and setup
├── README.md                 # Project documentation
├── requirements.txt          # Dependency list
├── rules.py                  # Real-time feature engineering & risk scoring
└── transaction_simulator.py  # Simulated telemetry stream generator


## 📊 Live Dashboard & Pipeline Demo

![Fraud Shield Live Dashboard](/Users/gunjan.kumar/Documents/TransactionFraudShield-Pipeline/docs/assets/Screenshot 2026-09-21 at 10.18.08 PM.png)
![Fraud Shield Live Dashboard](/Users/gunjan.kumar/Documents/TransactionFraudShield-Pipeline/docs/assets/Screenshot 2026-09-21 at 10.18.41 PM.png)
![Fraud Shield Live Dashboard](/Users/gunjan.kumar/Documents/TransactionFraudShield-Pipeline/docs/assets/Screenshot 2026-09-21 at 10.18.56 PM.png)
![Fraud Shield Live Dashboard](/Users/gunjan.kumar/Documents/TransactionFraudShield-Pipeline/docs/assets/Screenshot 2026-09-21 at 10.19.21 PM.png)
![Fraud Shield Live Dashboard](/Users/gunjan.kumar/Documents/TransactionFraudShield-Pipeline/docs/assets/Screenshot 2026-09-21 at 10.19.43 PM.png)