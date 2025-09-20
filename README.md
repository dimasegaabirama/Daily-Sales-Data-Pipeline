# 📊 Daily Sales Data Pipeline with Airflow, Snowflake, and dbt

An ETL/ELT pipeline for **retail supply chain analytics**, built with:

- **Apache Airflow** → workflow orchestrator  
- **Snowflake** → main data warehouse  
- **dbt (data build tool)** → transformation, snapshotting, testing  
- **MySQL** → operational database as the data source  

---

## 🚀 Key Features
- Automated schema and table creation in Snowflake  
- Extract data from MySQL (dimension & fact tables)  
- Load data into the *landing* schema in Snowflake using **Pandas + SQLAlchemy**  
- Modular pipeline (`extract.py`, `load.py`, `connection.py`, etc.) → easy to maintain  
- Configurable via **Airflow Variables** (`secret_file`, `sql_file`, etc.)  
- **dbt tasks** automatically executed in a single task group:
  - `test_source` → validate sources  
  - `run` → run transformations  
  - `test_model` → test model outputs  
  - `snapshot` → perform snapshotting  

---

## 📂 Project Structure
```bash
.
├── airflow/
│   ├── dags/
│   │   └── daily_sales.py 
│   ├── include/
│   │   ├── config/
│   │   │   ├── .secrets.toml 
│   │   │   └── airflow_settings.yaml
│   │   ├── etl/
│   │   │   ├── connection.py 
│   │   │   ├── extract.py 
│   │   │   ├── load.py 
│   │   │   ├── transform.py
│   │   │   └── utils.py 
│   │   └── sql/
│   │       └── create_table.sql
│   ├── tests/
│   │   └── dags/
│   │       └── test_dag_example.py
│   ├── .dockerignore
│   ├── docker-compose.override.yml
│   ├── Dockerfile
│   ├── packages.txt
│   └── requirements.txt
│  
├── dbt/
│   └── my_snowflake_db/
│       ├── analyses/ 
│       ├── macros/
│       │   └── generate_schema_name.sql  
│       ├── models/
│       │   ├── dimension/
│       │   │   ├── dim_date.sql
│       │   │   ├── dim_products.sql
│       │   │   ├── dim_suppliers.sql
│       │   │   └── dim_warehouse.sql
│       │   ├── fact/
│       │   │   ├── fact_inventory.sql
│       │   │   ├── fact_orders.sql
│       │   │   ├── fact_sales.sql
│       │   │   └── fact_shipments.sql
│       │   └── schema_warehouse.yml
│       ├── seeds/
│       ├── snapshots/
│       │   ├── dim_product_snapshot.sql
│       │   ├── dim_supplier_snapshot.sql
│       │   └── dim_warehouse_snapshot.sql
│       ├── tests/
│       │   ├── generic/
│       │   │   ├── test_string_and_set.sql
│       │   │   ├── test_validate_fact_inventory_arrays.sql
│       │   │   └── test_validate_id_date.sql
│       │   └── singular/
│       ├── .gitignore
│       ├── dbt_project.yml
│       ├── package-lock.yml
│       ├── packages.yml
│       └── profiles.yml
│
├── docs/
│   ├── pipeline.png
│   └── schema_source.png
│
├── .gitignore
└── README.md
```
---

## ⚙️ How It Works
- **Airflow DAG** (`daily_sales.py`) orchestrates the pipeline:
    - Creates schemas/tables in Snowflake
    - Extracts data from MySQL
    - Loads raw data into Snowflake (landing schema)
    - Executes dbt tasks for transformation, testing, and snapshotting
- **Configuration** is managed via:
    - Airflow Variables (paths & secrets)
    - .secrets.toml for credentials (not committed to Git)
- **dbt Project** handles transformations and quality checks, ensuring data is production-ready.

---

## 🛠️ Tech Stack

- Airflow `2.x`
- Snowflake
- dbt Core `1.x`
- MySQL
- Python `3.9+`
- Pandas + SQLAlchemy

---

## 📊 Pipeline, Database & BI Overview

**Pipeline Flow:**  
![Pipeline Diagram](docs/pipeline.png)

**Source Schema (MySQL)**
![Source Schema](docs/schema_source.png)

**Warehouse Schema (Snowflake)**
![Warehouse Schema](docs/schema_warehouse.png)

**Dashboard:**  
This shows sample visualizations based on the data loaded into Snowflake and transformed via dbt.  
![Power BI Dashboard](docs/powerbi_dashboard.png)

---
## 🔑 Portfolio Highlights

- Demonstrates end-to-end retail data pipeline
- Shows integration of Airflow, Snowflake, dbt, and Python ETL scripts
- Includes modular ETL, snapshotting, and automated data quality testing
- Fully documented and ready to showcase on GitHub

---

