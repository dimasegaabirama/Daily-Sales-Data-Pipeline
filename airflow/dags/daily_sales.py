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
from airflow.operators.python import get_current_context
from airflow.models import Variable


# timezone default
local_tz = pendulum.timezone("Asia/Jakarta")

default_args = {
    "retries" : 2,
    "retry_delay" : pendulum.duration(minutes=2)
}

@dag(
    start_date=pendulum.datetime(2025, 8, 29, tz=local_tz),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
    dagrun_timeout=pendulum.duration(minutes=30),
    max_active_runs=1,              # DAG run yang boleh aktif
    max_active_tasks=5,             # TI yg boleh aktif pda 1 dag run
    max_consecutive_failed_dag_runs=2,
    tags=["dbt", "daily_sales"]
)
def daily_sales():

    sql_file = Variable.get("sql_file", default_var=None, deserialize_json=True)    
    dbt_path = Variable.get("dbt_path", default_var=None, deserialize_json=True)
    
    create_schema = Path(sql_file["create_schema"])
    fact_queries = Path(sql_file["fact_queries"])
    dim_queries = Path(sql_file["dim_queries"])
    
    profile_path = dbt_path["profile_path"]
    project_path = dbt_path["project_path"]

    snowflake_conn = get_snowflake_conn("warehouse")
    database_conn = get_database_conn("retail_supply_chain", "mysql")

    @task()
    def create_table():
        create_table_snowflake(snowflake_conn,create_schema)

    @task(max_active_tis_per_dag=1)
    def load_dimension():
        elt_pipeline(
            path_file = dim_queries,
            source_conn = database_conn,
            snowflake_conn = snowflake_conn,
            schema = "landing",
            type = "dimension"
            )

    @task(max_active_tis_per_dag=1)
    def load_fact():
        context = get_current_context()
        ds = context["ds"]

        try:
            prev_ds = context["prev_ds"]
        except KeyError:
            prev_ds = str(pendulum.parse(ds).subtract(days=1).date())

        print("ds:", ds)
        print("prev_ds:", prev_ds)
        
        elt_pipeline(
            path_file = fact_queries,
            source_conn = database_conn,
            snowflake_conn = snowflake_conn,
            schema = "landing",
            type = "fact",
            prev_ds = prev_ds,
            ds = ds
            )
        
    @task_group(group_id = "dbt_run_group")
    def dbt_run_group():
        dbt_test_source = make_dbt_task(
                        task_id = "test_source",
                        command = ["test", "--select", "source:*"],
                        profile_path = profile_path,
                        project_path = project_path
                        )
        dbt_run = make_dbt_task(
                    task_id = "run_task",
                    command = ["run"],
                    profile_path = profile_path,
                    project_path = project_path
                    )
        dbt_test_model = make_dbt_task(
                    task_id = "test_model",
                    command = ["test", "--select", "path:models/*"],
                    profile_path = profile_path,
                    project_path = project_path
                    )
        dbt_snapshot = make_dbt_task(
                    task_id = "snapshot",
                    command = ["snapshot"],
                    profile_path = profile_path,
                    project_path = project_path
                    )

        dbt_test_source >> dbt_run >> dbt_test_model >> dbt_snapshot

    create_table() >> load_dimension() >> load_fact() >> dbt_run_group()

daily_sales()
