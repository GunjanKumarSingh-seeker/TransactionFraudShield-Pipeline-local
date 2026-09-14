# Setup Guide

This guide takes you from a fresh clone to a working fraud analytics dashboard.

## 1. Clone Repository
```bash
git clone [https://github.com/GunjanKumarSingh-seeker/TransactionFraudShield-Pipeline.git](https://github.com/GunjanKumarSingh-seeker/TransactionFraudShield-Pipeline.git)
cd TransactionFraudShield-Pipeline
```
## 2. Create Python Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
```
## 3. Environment Configuration
```bash
cp .env.example .env
```

## 4. Run Offline Demo
Generate synthetic telemetry data and process Bronze, Silver, and Gold layers:
```bash
bash scripts/generate_offline_demo_data.sh
```

## 5. Start Dashboard
Launch the interactive Dash web dashboard:
```bash
python -m fraud_shield.dashboard.app
```
Open your browser at: http://localhost:8060

## 6. Run Tests
Verify feature calculations, data quality rules, and risk scoring:

```bash
python -m pytest tests/
```

## 7. Kafka Mode (Optional Containerized Execution)

# Start Docker services
```
docker compose up -d kafka minio minio-init postgres
```
# Initialize topics and run producers/consumers
```
bash scripts/init_kafka_topics.sh
python -m fraud_shield.producers.transaction_simulator --event-rate 20 --duration 60 --fraud-rate 12
python -m fraud_shield.consumers.landing_consumer --landing-root data/landing
bash scripts/run_local_pipeline.sh
```
## 8. Reset Local Data

```bash
make clean
```

