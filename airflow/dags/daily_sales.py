import pendulum
from pathlib import Path

from include.etl import (
    get_database_conn,
    get_snowflake_conn,
    create_table_snowflake,
    elt_pipeline,
    make_dbt_task
)

from airflow.decorators import dag, task, task_group
from airflow.exceptions import AirflowFailException
from airflow.models import Variable


# timezone default
local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    "retries" : 2,
    "retry_delay" : pendulum.duration(minutes=2)
}

@dag(
    start_date=pendulum.datetime(2025, 8, 29, tz=local_tz),
    schedule=None,
    catchup=False,
    default_args=default_args,
    dagrun_timeout=pendulum.duration(minutes=30),
    max_active_runs=1,              # DAG run yang boleh aktif
    max_active_tasks=5,             # TI yg boleh aktif pda 1 dag run
    max_consecutive_failed_dag_runs=2,
    tags=["dbt", "daily_sales"]
)
def daily_sales():
    table_dimension = ["products", "warehouses", "suppliers"]
    table_fact = ["shipments", "shipmentitems", "orders", "orderitems", "sales", "stock"]

    # path
    secret_file = Path(Variable.get("secret_file", default_var=None))
    
    sql_file = Variable.get("sql_file", default_var=None, deserialize_json=True)
    
    create_schema = Path(sql_file["create_schema"])
    fact_queries = Path(sql_file["fact_queries"])
    dim_queries = Path(sql_file["dim_queries"])

    # koneksi database
    snowflake_conn = get_snowflake_conn(secret_file)
    database_conn = get_database_conn(secret_file, "mysql")

    @task()
    def create_table():
        create_table_snowflake(snowflake_conn,create_schema)

    @task(max_active_tis_per_dag=1)
    def load_dimension():
        elt_pipeline(path_file = dim_queries,
                     source_conn = database_conn,
                     snowflake_conn = snowflake_conn,
                     schema = "landing",
                     type = "dimension"
                     )

    @task(max_active_tis_per_dag=1)
    def load_fact():
        elt_pipeline(path_file = fact_queries,
                     source_conn = database_conn,
                     snowflake_conn = snowflake_conn,
                     schema = "landing",
                     type = "fact",
                     )

    @task_group(group_id="dbt_run_group")
    def dbt_run_group():

        dbt_test_source = make_dbt_task(
                        task_id="test_source",
                        command=["test", "--select", "source:*"]
                    )
        dbt_run = make_dbt_task(
                    task_id="run_task",
                    command=["run"]
                )
        dbt_test_model = make_dbt_task(
                    task_id="test_model",
                    command=["test", "--select", "path:models/*"]
                )
        dbt_snapshot = make_dbt_task(
                    task_id="snapshot",
                    command=["snapshot"]
                )

        dbt_test_source >> dbt_run >> dbt_test_model >> dbt_snapshot

    create_table() >> load_dimension() >> load_fact() >> dbt_run_group()

daily_sales()
