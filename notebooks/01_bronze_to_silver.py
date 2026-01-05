# Databricks notebook source
# MAGIC %md
# MAGIC # 01 - Bronze to Silver (Clean & Standardize)
# MAGIC
# MAGIC **Inputs:** raw CSV/JSON files in ADLS Gen2 Bronze
# MAGIC **Outputs:** cleaned parquet/delta in Silver

# COMMAND ----------

from pyspark.sql import functions as F

# COMMAND ----------

# Widgets (set these in ADF Databricks activity parameters)
dbutils.widgets.text("bronze_path", "abfss://bronze@<storage>.dfs.core.windows.net/user_activity/")
dbutils.widgets.text("silver_path", "abfss://silver@<storage>.dfs.core.windows.net/user_activity/")
bronze_path = dbutils.widgets.get("bronze_path")
silver_path = dbutils.widgets.get("silver_path")

# COMMAND ----------

# Read raw (CSV example). For JSONL use spark.read.json(...)
df = (
    spark.read.option("header", True)
    .csv(bronze_path)
)

# COMMAND ----------

# Standardize schema
df2 = (
    df
    .withColumn("user_id", F.col("user_id").cast("int"))
    .withColumn("event_type", F.trim(F.lower(F.col("event_type"))))
    .withColumn("device", F.trim(F.lower(F.col("device"))))
    .withColumn("event_time_ts", F.to_timestamp("event_time"))
    .drop("event_time")
    .withColumnRenamed("event_time_ts", "event_time")
    .withColumn("event_date", F.to_date("event_time"))
)

# Data quality checks
df2 = df2.dropna(subset=["user_id","event_type","event_time","device","session_id"]).dropDuplicates()

# COMMAND ----------

# Write Silver
(
    df2.write.mode("overwrite")
    .format("delta")
    .save(silver_path)
)

print(f"Wrote silver delta to: {silver_path}")
