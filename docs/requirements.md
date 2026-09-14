# Requirements

TransactionFraudShield Pipeline requires Python 3.10+ and standard local development tools. It runs entirely on your machine using local file storage or optional local Docker containers.

## Core Prerequisites

| Requirement | Recommended Version | Purpose |
| :--- | :---: | :--- |
| **Python** | 3.10+ | Runs stream simulator, feature engine, risk rules, tests, and dashboard. |
| **pip** | Latest | Package management. |
| **Git** | Latest | Version control and source management. |
| **Docker Desktop** | Optional | Containerization for optional local Kafka, MinIO, and Postgres services. |

---

## Environment Setup

1. **Create and Activate Virtual Environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   
2. **Install Project Dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -e .

4. **Verify Setup:**
   ```bash
   python -m pytest tests/