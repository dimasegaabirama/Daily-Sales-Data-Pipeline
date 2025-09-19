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

## 📂 Struktur Proyek

.
├── dags/
│ └── daily_sales.py 
├── include/
│ ├── config/
│ │ ├── .secrets.toml 
│ │ └── airflow_settings.yaml
│ ├── etl/
│ │ ├── connection.py 
│ │ ├── extract.py 
│ │ ├── load.py 
│ │ ├── transform.py
│ │ └── utils.py 
│ └── sql/
│   └── create_table.sql
├── tests/
│ └── dags/
│   └── test_dag_example.py
│
├── .dockerignore
├── .gitignore
├── docker-compose.override.yml
├── dockerfile
├── packages.txt
├── requirements.txt
└── README.md

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


