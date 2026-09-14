# Data Quality Framework

TransactionFraudShield Pipeline enforces data quality checks at the ingestion layer before writing data to Silver tables. Data validation failures are logged to maintain metrics visibility across the lakehouse.

---

## 1. Quality Check Suite

The quality suite evaluates datasets against critical integrity rules:

| Entity | Check Name | Check Condition | Severity | Failure Action |
| :--- | :--- | :--- | :---: | :--- |
| **Transactions** | `event_id_present` | `event_id` is NOT null | Critical | Flagged / Quarantined |
| **Transactions** | `event_timestamp_present` | `event_timestamp` is NOT null | Critical | Flagged / Quarantined |
| **Transactions** | `customer_id_present` | `customer_id` is NOT null | Critical | Flagged / Quarantined |
| **Transactions** | `transaction_id_present` | `transaction_id` is NOT null | Critical | Flagged / Quarantined |
| **Transactions** | `amount_non_negative` | `amount` >= 0 | Critical | Flagged / Quarantined |
| **Transactions** | `valid_ip_country` | `ip_country` code length == 2 | Warning | Logged |
| **Transactions** | `valid_billing_country` | `billing_country` code length == 2 | Warning | Logged |

---

## 2. Quality Metrics & Reporting

Quality check results are compiled into summary metrics and saved to the Gold layer table (`gold_data_quality_summary`):

* **`total_record_count`**: Total records evaluated.
* **`failed_record_count`**: Number of records violating the check condition.
* **`passed_record_count`**: Number of valid records.
* **`pass_percentage`**: Ratio of valid records ($\text{passed} / \text{total}$).
* **`dq_status`**: `pass` if pass percentage meets quality threshold, else `fail`.

---

## 3. Pipeline Execution

Data quality checks are executed in `fraud_shield/pipeline/quality/checks.py`:

```python
from fraud_shield.pipeline.quality.checks import fraud_checks

# Evaluates transaction dataframe and returns summary quality status
dq_results_df = fraud_checks(transactions_df)