# Data Contracts & Schema Governance

Data contracts ensure strict schema validation and prevent breaking changes or schema drift from impacting downstream Bronze, Silver, and Gold medallion layers.


## 1. Registered Data Streams

Each streaming topic in the pipeline is enforced against an explicit JSON schema contract located in `data_contracts/`:

| Stream Name | Target Kafka Topic / Event Source | Schema Contract Path |
| :--- | :--- | :--- |
| **Transactions** | `fraud_transactions` | `data_contracts/transactions_schema.json` |
| **Logins** | `fraud_logins` | `data_contracts/logins_schema.json` |
| **Devices** | `fraud_devices` | `data_contracts/devices_schema.json` |
| **Chargebacks** | `fraud_chargebacks` | `data_contracts/chargebacks_schema.json` |


## 2. Core Contract Principles

* **Universal Event Identifiers:** Every incoming payload must contain a valid `event_id` and ISO-8601 formatted `event_timestamp`.
* **ID Preservation:** Mandatory entity keys (`customer_id`, `device_id`, `merchant_id`, `transaction_id`) are preserved across ingestion.
* **Raw Preservation (Bronze):** Raw payloads are written directly to Bronze storage prior to any schema validation or transformations.
* **Schema Enforcement & Quarantine (Silver):** Records failing strict schema validation are quarantined into isolation paths with error reason codes attached.

## 3. Importance in Fraud Analytics

In production fraud platforms, unannounced schema changes (such as missing timestamps, null customer IDs, or corrupted numerical formats) cause silent monitoring failures. Data contracts enforce strict boundaries in the Silver layer, isolating invalid records into quarantine while maintaining uninterrupted pipeline execution.