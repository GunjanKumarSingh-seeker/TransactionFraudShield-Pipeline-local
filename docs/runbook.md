# End-to-End Runbook

## 1. Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .
cp .env.example .env
```

## 2. Offline Demo (No Kafka Required)

# Generate sample telemetry and process Bronze -> Silver -> Gold tables
```
bash scripts/generate_offline_demo_data.sh
```

# Start dashboard
```
python -m fraud_shield.dashboard.app
```

Open dashboard at `http://localhost:8060`.

## 3. Containerized / Kafka Mode

```bash
make up
make init
make produce
make consume
make run-pipeline
make dashboard
```

## 4. Pipeline Validation & Tests
Empty Dashboard: If the dashboard shows no records, run the offline generator to populate Gold tables:
```bash
bash scripts/generate_offline_demo_data.sh
```

Kafka Cluster Not Ready: Wait 20–30 seconds after running make up before calling `make init`.

Clean Data State: To wipe local outputs and reset state:
`make clean`