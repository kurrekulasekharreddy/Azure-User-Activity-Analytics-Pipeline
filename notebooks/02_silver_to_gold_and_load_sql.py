# Databricks notebook source
# MAGIC %md
# MAGIC # 02 - Silver to Gold (Aggregates) + Load to Azure SQL/Synapse
# MAGIC
# MAGIC **Inputs:** Silver delta table
# MAGIC **Outputs:** Gold aggregates in ADLS + optional load to Azure SQL/Synapse

# COMMAND ----------

from pyspark.sql import functions as F

dbutils.widgets.text("silver_path", "abfss://silver@<storage>.dfs.core.windows.net/user_activity/")
dbutils.widgets.text("gold_path", "abfss://gold@<storage>.dfs.core.windows.net/user_activity/")
dbutils.widgets.text("sql_jdbc_url", "")  # e.g., jdbc:sqlserver://<server>:1433;database=<db>;encrypt=true;...
dbutils.widgets.text("sql_user", "")
dbutils.widgets.text("sql_password", "")

silver_path = dbutils.widgets.get("silver_path")
gold_path = dbutils.widgets.get("gold_path")

# COMMAND ----------

silver_df = spark.read.format("delta").load(silver_path)

# DAU
dau = (
    silver_df.groupBy("event_date")
    .agg(F.countDistinct("user_id").alias("dau"))
)

# Events by type
by_type = (
    silver_df.groupBy("event_date", "event_type")
    .agg(F.count("*").alias("event_count"))
)

# Events by device
by_device = (
    silver_df.groupBy("event_date", "device")
    .agg(F.count("*").alias("event_count"))
)

# COMMAND ----------

# Write gold datasets
(dau.write.mode("overwrite").format("delta").save(f"{gold_path}/daily_user_metrics"))
(by_type.write.mode("overwrite").format("delta").save(f"{gold_path}/daily_event_type_metrics"))
(by_device.write.mode("overwrite").format("delta").save(f"{gold_path}/daily_device_metrics"))

print("Wrote gold delta datasets.")

# COMMAND ----------

# Optional: load into Azure SQL/Synapse using JDBC
jdbc_url = dbutils.widgets.get("sql_jdbc_url").strip()
user = dbutils.widgets.get("sql_user").strip()
pwd = dbutils.widgets.get("sql_password").strip()

if jdbc_url and user and pwd:
    props = {"user": user, "password": pwd, "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"}

    (dau.write.mode("overwrite").jdbc(url=jdbc_url, table="dbo.daily_user_metrics", properties=props))
    (by_type.write.mode("overwrite").jdbc(url=jdbc_url, table="dbo.daily_event_type_metrics", properties=props))
    (by_device.write.mode("overwrite").jdbc(url=jdbc_url, table="dbo.daily_device_metrics", properties=props))

    print("Loaded gold tables into SQL.")
else:
    print("SQL load skipped (missing JDBC settings).")
