import json
from datetime import datetime


def get_shift_period(timestamp):
    hour = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).hour

    if 5 <= hour < 12:
        return "morning"
    elif 12 <= hour < 17:
        return "afternoon"
    elif 17 <= hour < 22:
        return "evening"
    else:
        return "night"


def get_bus_category(bus_id):
    number = int(bus_id.split("-")[1])

    if number <= 70:
        return "electric"
    elif number <= 140:
        return "hybrid"
    else:
        return "diesel"


def lambda_handler(event, context):
    enriched_records = []

    for record in event:
        body = json.loads(record["body"])

        body["shift_period"] = get_shift_period(body["timestamp"])
        body["bus_category"] = get_bus_category(body["bus_id"])
        body["event_date"] = body["timestamp"][:10]

        enriched_records.append(body)

    return enriched_records
