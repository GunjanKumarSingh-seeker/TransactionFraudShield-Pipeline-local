# Architecture

TransactionFraudShield Pipeline is a local-first, production-patterned fraud analytics platform. Local mode utilizes Docker Kafka and local storage under `data/`, allowing end-to-end pipeline execution without external cloud dependencies.

---

## Design Principles

* **Raw Event Preservation:** Ingest raw payloads into Bronze storage prior to transformation.
* **Medallion Separation:** Strict decoupling of raw (Bronze), validated/scored (Silver), and analytical serving (Gold) layers.
* **Quarantine-First Validation:** Schema drift or invalid payloads are isolated into quarantine tables rather than silently dropped.
* **Explainable Risk Scoring:** Rule triggers append granular reason codes alongside composite risk scores.
* **Business-Driven Gold Aggregations:** Gold tables are pre-aggregated around executive KPIs, risk hotspots, customer 360 profiles, and data quality metrics.

---

## Platform Layers

1. **Event Simulation:** Generates synthetic transaction, login, device, and chargeback telemetry.
2. **Streaming Ingestion:** Kafka event bus decouples ingestion across operational domains.
3. **Landing & Bronze:** Raw JSON payloads ingested with audit metadata (`ingested_at`, `source_topic`).
4. **Silver Layer:** Schema validation, type casting, deduplication, and quality check enforcement.
5. **Fraud Engine:** Heuristic risk rules score transactions (0–100) and assign risk bands (`LOW`, `MEDIUM`, `HIGH`).
6. **Gold Layer:** Business aggregates (daily volume, merchant risk hotspots, customer 360, DQ scorecard).
7. **Serving:** Interactive Plotly Dash dashboard for real-time monitoring and alerting.

---

## Scalability & Production Alignment

* **Decoupled Architecture:** Storage paths and ingestion modules are modular, supporting drop-in replacement with cloud object storage or managed streaming platforms.
* **Engine Agnostic Processing:** Pipeline modules are structured cleanly to allow seamless adaptation from local Python processing to distributed compute engines.