import json
import boto3
import os
import uuid

s3 = boto3.client("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]


def lambda_handler(event, context):
    written_files = []

    for record in event:
        event_date = record["event_date"]
        route_id = record["route_id"]
        event_type = record["event_type"]

        key = (
            f"raw/event_date={event_date}/"
            f"route_id={route_id}/"
            f"event_type={event_type}/"
            f"{uuid.uuid4()}.json"
        )

        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=key,
            Body=json.dumps(record),
            ContentType="application/json"
        )

        written_files.append(key)

    return {
        "statusCode": 200,
        "files_written": written_files
    }
