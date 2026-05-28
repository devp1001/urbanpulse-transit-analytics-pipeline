import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import col, when, sum as spark_sum, avg, count

args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "DATABASE_NAME", "RAW_TABLE_NAME", "OUTPUT_PATH"]
)

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

database_name = args["DATABASE_NAME"]
raw_table_name = args["RAW_TABLE_NAME"]
output_path = args["OUTPUT_PATH"]

dynamic_frame = glueContext.create_dynamic_frame.from_catalog(
    database=database_name,
    table_name=raw_table_name,
    transformation_ctx="raw_source"
)

df = dynamic_frame.toDF()

summary_df = df.groupBy("route_id", "event_date").agg(
    spark_sum(
        when(
            col("event_type") == "passenger_count",
            col("payload.tap_ins")
        ).otherwise(0)
    ).alias("total_passenger_tap_ins"),

    avg(
        when(
            col("event_type") == "fuel_reading",
            col("payload.fuel_level_percent")
        )
    ).alias("average_fuel_level"),

    count(
        when(col("event_type") == "gps_ping", True)
    ).alias("gps_ping_count"),

    count("*").alias("total_events")
)

summary_df.write \
    .mode("append") \
    .partitionBy("event_date") \
    .parquet(output_path)

job.commit()
