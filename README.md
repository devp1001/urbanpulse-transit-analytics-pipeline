# UrbanPulse Transit - City Bus Fleet Analytics Pipeline

## Project Overview

UrbanPulse Transit is a serverless AWS data engineering project for public transportation fleet analytics. The pipeline simulates city bus IoT telemetry, filters and enriches useful events, stores raw data in Amazon S3, catalogs the data with AWS Glue, and produces route-level daily analytics summaries.

## Architecture

```text
Mock Data Generator Lambda
        ↓
Amazon SQS Queue
        ↓
EventBridge Pipe
        ↓
Filter: gps_ping, passenger_count, fuel_reading
        ↓
Enrichment Lambda
        ↓
S3 Writer Lambda
        ↓
Amazon S3 Raw Zone
        ↓
Glue Raw Crawler
        ↓
Glue Data Catalog Raw Table
        ↓
Glue ETL Job with Bookmarking
        ↓
Amazon S3 Processed Zone
        ↓
Glue Processed Crawler
        ↓
Final Analytics Table
```

## AWS Services Used

- AWS Lambda
- Amazon SQS
- Amazon EventBridge Pipes
- Amazon S3
- AWS Glue Crawler
- AWS Glue Data Catalog
- AWS Glue ETL Job
- IAM
- CloudWatch Logs

## Resource Names

| Resource | Name |
|---|---|
| S3 Bucket | `urbanpulse-transit-dev-devpatel` |
| SQS Queue | `urbanpulse-telemetry-queue` |
| Mock Lambda | `urbanpulse-mock-generator` |
| Enrichment Lambda | `urbanpulse-enrichment-lambda` |
| S3 Writer Lambda | `urbanpulse-s3-writer-lambda` |
| EventBridge Pipe | `urbanpulse-telemetry-pipe` |
| Glue Database | `urbanpulse_transit_db` |
| Raw Crawler | `urbanpulse-raw-crawler` |
| Raw Table | `raw_raw` |
| Glue ETL Job | `urbanpulse-route-summary-job` |
| Processed Crawler | `urbanpulse-processed-crawler` |

## S3 Folder Structure

```text
urbanpulse-transit-dev-devpatel/
├── raw/
├── processed/
└── scripts/
```

Raw data is stored using partitioned folders:

```text
raw/event_date=YYYY-MM-DD/route_id=RT-XX/event_type=event_type/file.json
```

Processed data is stored as Parquet:

```text
processed/event_date=YYYY-MM-DD/part-000.parquet
```

## Event Types

The mock generator creates these event types:

- `gps_ping`
- `passenger_count`
- `fuel_reading`
- `engine_diagnostic`
- `schedule_check`
- `door_sensor`

The EventBridge Pipe keeps only these analytics events:

- `gps_ping`
- `passenger_count`
- `fuel_reading`

## Enrichment Logic

The enrichment Lambda adds:

| Field | Description |
|---|---|
| `shift_period` | morning, afternoon, evening, or night based on timestamp |
| `bus_category` | electric, hybrid, or diesel based on bus ID |
| `event_date` | date extracted from timestamp |

## Glue ETL Output Metrics

For each route and date, the Glue job calculates:

| Metric | Meaning |
|---|---|
| `total_passenger_tap_ins` | Total passengers boarding buses |
| `average_fuel_level` | Average fuel percentage |
| `gps_ping_count` | Number of GPS ping events |
| `total_events` | Total events processed |

## Glue Job Parameters

| Key | Value |
|---|---|
| `--DATABASE_NAME` | `urbanpulse_transit_db` |
| `--RAW_TABLE_NAME` | `raw_raw` |
| `--OUTPUT_PATH` | `s3://urbanpulse-transit-dev-devpatel/processed/` |
| `--job-bookmark-option` | `job-bookmark-enable` |

## Job Bookmarking

Job bookmarking is enabled so the Glue ETL job processes only new/unprocessed data in future runs. This helps avoid duplicate processing and duplicate summaries.

## Screenshots to Include

Place screenshots in the `screenshots/` folder:

1. S3 bucket folders
2. SQS queue
3. Mock Lambda test success
4. EventBridge Pipe configuration
5. Raw S3 partition folders
6. Raw Glue crawler success
7. Raw Glue table schema and partitions
8. Glue job parameters
9. Glue job successful run
10. Processed S3 output
11. Processed crawler success
12. Processed Glue table

## Cost Control

To stop major costs:

1. Stop the EventBridge Pipe.
2. Purge SQS messages.
3. Make sure Glue ETL job is not running.

Glue jobs only create significant cost while running.

## Conclusion

This project demonstrates a real-world serverless data engineering pipeline using AWS. It covers ingestion, filtering, enrichment, data lake storage, cataloging, ETL processing, partitioning, and analytics-ready output.
