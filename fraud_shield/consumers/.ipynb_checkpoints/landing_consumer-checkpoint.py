from __future__ import annotations

import argparse
from datetime import date

try:
    from kafka import KafkaConsumer
except Exception:  # pragma: no cover
    KafkaConsumer = None

from fraud_shield.pipeline.utils.io import write_jsonl
from fraud_shield.topics import TOPIC_NAMES


def consume_to_landing(bootstrap_servers: str, landing_root: str, max_messages: int = 1000, batch_size: int = 50) -> int:
    if KafkaConsumer is None:
        raise RuntimeError("kafka-python is not installed.")

    topics = list(TOPIC_NAMES.values())
    consumer = KafkaConsumer(
        *topics,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        consumer_timeout_ms=8000,
        value_deserializer=lambda value: __import__("json").loads(value.decode("utf-8")),
    )

    counts: dict[str, list[dict]] = {}
    total = 0
    written = 0
    processing_date = date.today().isoformat()
    
    import time # Needed for unique file names

    for message in consumer:
        counts.setdefault(message.topic, []).append(message.value)
        total += 1
        
        # Micro-batching: write to disk every 'batch_size' messages
        if total % batch_size == 0:
            batch_timestamp = int(time.time() * 1000) # Unique ID for each batch file
            for topic, records in counts.items():
                # Write to a uniquely named file so the ETL loop doesn't block the stream
                path = f"{landing_root}/{topic}/processing_date={processing_date}/events_{batch_timestamp}.jsonl"
                written += write_jsonl(records, path)
            
            # Reset counts buffer after writing the batch
            counts.clear()

        if total >= max_messages:
            break

    # Flush any remaining messages when the loop breaks
    if counts:
        batch_timestamp = int(time.time() * 1000)
        for topic, records in counts.items():
            path = f"{landing_root}/{topic}/processing_date={processing_date}/events_{batch_timestamp}.jsonl"
            written += write_jsonl(records, path)

    return written


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Land Kafka events into replayable JSONL files.")
    parser.add_argument("--kafka-bootstrap-servers", default="localhost:9092")
    parser.add_argument("--landing-root", default="data/landing")
    parser.add_argument("--max-messages", type=int, default=1000)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    count = consume_to_landing(args.kafka_bootstrap_servers, args.landing_root, args.max_messages)
    print(f"Landed {count} events")


if __name__ == "__main__":
    main()
