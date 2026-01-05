# Azure User Activity Analytics Pipeline (End-to-End Data Engineering Project)

An end-to-end **Azure Data Engineering** project that ingests user-activity events (CSV/JSON), lands raw data in **ADLS Gen2 (Bronze)**, transforms it with **Azure Databricks (PySpark)** into **Silver/Gold** layers, loads curated metrics to **Azure SQL / Synapse**, and powers dashboards in **Power BI**.

> Built to be **GitHub portfolio-ready**: includes sample data, ingestion scripts, Databricks notebooks, SQL schema, and Azure Data Factory (ADF) templates.

---

## Architecture

```mermaid
flowchart TD
  A[Source: API/CSV/JSON] --> B[Azure Data Factory - Ingestion]
  B --> C[ADLS Gen2 - Bronze (raw)]
  C --> D[Azure Databricks - Transform (PySpark)]
  D --> E[ADLS Gen2 - Silver (clean)]
  E --> F[ADLS Gen2 - Gold (aggregates)]
  F --> G[Azure SQL DB / Synapse - Serving Layer]
  G --> H[Power BI - Dashboard]
  B --> I[Monitoring: ADF Logs/Azure Monitor]
  D --> I
  G --> I
```

---

## What you will build

- **Bronze**: Raw event files copied into ADLS Gen2
- **Silver**: Cleaned and standardized events (dedupe, null handling, timestamp parsing)
- **Gold**: Analytics-ready aggregates:
  - Daily Active Users (DAU)
  - Events per day by type
  - Events per day by device
- **Serving Layer**: Curated tables in Azure SQL DB / Synapse
- **Orchestration**: ADF pipeline (Copy -> Databricks notebook -> Load SQL)

---

## Tech Stack (Azure)

- **Azure Data Lake Storage Gen2 (ADLS)** – bronze/silver/gold zones
- **Azure Data Factory (ADF)** – orchestration + ingestion
- **Azure Databricks** – PySpark transformations
- **Azure SQL Database / Azure Synapse** – curated tables + SQL analytics
- **Power BI** – dashboards
- **Python + SQL** – ingestion utilities and schema

---

## Repository structure

```
.
├─ data/
│  ├─ sample_events.csv
│  ├─ sample_events.jsonl
│  └─ generate_sample_data.py
├─ infra/
│  └─ adf/
│     ├─ pipeline_user_activity.json
│     └─ linked_services_examples/
│        ├─ ls_adls_example.json
│        ├─ ls_databricks_example.json
│        └─ ls_azure_sql_example.json
├─ notebooks/
│  ├─ 01_bronze_to_silver.py
│  └─ 02_silver_to_gold_and_load_sql.py
├─ sql/
│  ├─ 00_create_schema.sql
│  ├─ 01_create_tables.sql
│  └─ 02_sample_queries.sql
├─ src/
│  ├─ __init__.py
│  ├─ config.py
│  ├─ upload_to_adls.py
│  └─ validate_data.py
├─ .env.example
├─ requirements.txt
└─ LICENSE
```

---

## Quickstart (Local)

### 1) Create a virtual environment & install deps
```bash
python -m venv .venv
source .venv/bin/activate   # mac/linux
# .venv\Scripts\activate  # windows
pip install -r requirements.txt
```

### 2) Generate sample data
```bash
python data/generate_sample_data.py --rows 5000
```

### 3) Validate locally (basic checks)
```bash
python -m src.validate_data --input data/sample_events.csv
```

### 4) Upload raw data to ADLS (Bronze)
1. Copy `.env.example` to `.env` and fill values.
2. Run:
```bash
python -m src.upload_to_adls --local-path data/sample_events.csv --remote-path bronze/user_activity/dt=$(date +%F)/sample_events.csv
```

---

## Azure Setup (High-level)

### A) Create Azure resources
- ADLS Gen2 storage account (enable hierarchical namespace)
- ADF instance
- Databricks workspace
- Azure SQL Database (or Synapse dedicated pool)

### B) Create ADLS containers
- `bronze`
- `silver`
- `gold`

### C) Configure ADF
Use the example templates under `infra/adf/`:
- Create Linked Services:
  - ADLS Gen2
  - Databricks
  - Azure SQL
- Import/Build pipeline:
  - **Copy Activity**: source -> `bronze/`
  - **Databricks Notebook Activity**: run `01_bronze_to_silver` then `02_silver_to_gold_and_load_sql`

> Note: ADF JSON differs slightly by region/versions. Treat these as **templates** and update resource IDs.

### D) Configure Databricks
- Create a cluster (runtime supporting Spark 3.x)
- Upload notebooks from `notebooks/`
- Set notebook widgets/parameters (paths, SQL connection)

### E) Create SQL schema & tables
Run scripts in `sql/`:
- `00_create_schema.sql`
- `01_create_tables.sql`

---

## Data model

### Raw event fields
- `user_id` (int)
- `event_type` (string) — login, click, view, purchase, logout
- `event_time` (timestamp)
- `device` (string) — mobile, web, tablet
- `session_id` (string)

### Curated metrics (Gold)
- Daily Active Users (DAU)
- Counts by event_type
- Counts by device

---

## How to talk about this in interviews

- Explain the **bronze/silver/gold** pattern and why it matters
- Describe how you ensured **data quality** (schema checks, null checks, dedupe)
- Mention orchestration with **ADF** and compute with **Databricks**
- Discuss serving layer decisions (**Synapse/SQL**) and BI consumption (**Power BI**)

---

## License
MIT (see `LICENSE`)
