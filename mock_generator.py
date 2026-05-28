import json
import boto3
import os
import random
from datetime import datetime, timezone

sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]

EVENT_TYPES = [
    "gps_ping",
    "passenger_count",
    "fuel_reading",
    "engine_diagnostic",
    "schedule_check",
    "door_sensor"
]

ROUTES = [f"RT-{i:02d}" for i in range(1, 13)]


def build_payload(event_type):
    if event_type == "gps_ping":
        return {
            "latitude": round(random.uniform(41.70, 42.05), 6),
            "longitude": round(random.uniform(-87.90, -87.50), 6),
            "speed_mph": random.randint(0, 55)
        }

    if event_type == "passenger_count":
        return {
            "tap_ins": random.randint(0, 35),
            "tap_outs": random.randint(0, 30)
        }

    if event_type == "fuel_reading":
        return {
            "fuel_level_percent": random.randint(10, 100)
        }

    if event_type == "engine_diagnostic":
        return {
            "engine_temp": random.randint(150, 230),
            "error_code": random.choice(["NONE", "E101", "E202"])
        }

    if event_type == "schedule_check":
        return {
            "delay_minutes": random.randint(-5, 25)
        }

    return {
        "door_open": random.choice([True, False])
    }


def lambda_handler(event, context):
    messages_sent = 0

    for _ in range(25):
        event_type = random.choice(EVENT_TYPES)

        message = {
            "bus_id": f"BUS-{random.randint(1, 200):03d}",
            "route_id": random.choice(ROUTES),
            "event_type": event_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "payload": build_payload(event_type)
        }

        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        messages_sent += 1

    return {
        "statusCode": 200,
        "body": f"Sent {messages_sent} telemetry messages"
    }
