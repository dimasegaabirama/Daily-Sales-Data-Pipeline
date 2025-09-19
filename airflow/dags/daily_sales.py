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
    max_active_tasks=2,             # TI yg boleh aktif pda 1 dag run
    max_consecutive_failed_dag_runs=2,
    tags=["dbt", "daily_sales"]
)
def daily_sales():
    table_dimension = ["products", "warehouses", "suppliers"]
    table_fact = ["shipments", "shipmentitems", "orders", "orderitems", "sales", "stock"]

    # path
    secret_file = Path(Variable.get("secret_file", default_var=None))
    
    sql_file = Variable.get("sql_file", default_var=None, deserialize_json=True)
    create_schema = Path(sql_file["create_table"])

    # koneksi database
    snowflake_conn = get_snowflake_conn(secret_file)
    database_conn = get_database_conn(secret_file, "mysql")

    @task()
    def create_table():
        create_table_snowflake(snowflake_conn,create_schema)

    @task(max_active_tis_per_dag=1)
    def load_dimension():
        elt_pipeline(table_names = table_dimension,
                     source_conn = database_conn,
                     snowflake_conn = snowflake_conn,
                     schema = "landing",
                     type = "dimension"
                     )

    @task(max_active_tis_per_dag=1)
    def load_fact():
        queries = {
            "orderitems": """
                WITH cte_order AS (
                    SELECT orderid
                    FROM RETAIL_SUPPLY_CHAIN.Orders 
                    WHERE orderdate BETWEEN '{{ prev_ds }}' AND '{{ ds }}'
                )
                SELECT
                    oi.OrderItemID,
                    oi.OrderID,
                    oi.ProductID,
                    oi.Quantity,
                    oi.Price
                FROM RETAIL_SUPPLY_CHAIN.OrderItems oi 
                WHERE oi.OrderID IN (SELECT orderid FROM cte_order)
                """,
            "orders": """
                WITH cte_order AS (
                    SELECT 
                        orderid,
                        orderdate,
                        customername,
                        customeraddress
                    FROM RETAIL_SUPPLY_CHAIN.Orders o 
                    WHERE orderdate BETWEEN '{{ prev_ds }}' AND '{{ ds }}'
                )
                SELECT * FROM cte_order
                """,
            "sales": """
                SELECT
                    s.SaleID,
                    s.SaleDate,
                    s.ProductID,
                    s.Quantity,
                    s.TotalAmount
                FROM RETAIL_SUPPLY_CHAIN.Sales s 
                WHERE s.SaleDate BETWEEN '{{ prev_ds }}' AND '{{ ds }}'
                """,
            "shipmentitems": """
                WITH cte_shipment AS (
                    SELECT ShipmentID
                    FROM RETAIL_SUPPLY_CHAIN.Shipments 
                    WHERE ShipmentDate BETWEEN '{{ prev_ds }}' AND '{{ ds }}'
                )
                SELECT 
                    si.ShipmentItemID,
                    si.ShipmentID,
                    si.ProductID,
                    si.Quantity
                FROM RETAIL_SUPPLY_CHAIN.ShipmentItems si 
                WHERE si.ShipmentID IN (SELECT ShipmentID FROM cte_shipment)   
                """,
            "shipments": """
                WITH cte_shipment AS (
                    SELECT
                        ShipmentID,
                        SupplierID,
                        WarehouseID,
                        ShipmentDate
                    FROM RETAIL_SUPPLY_CHAIN.Shipments 
                    WHERE ShipmentDate BETWEEN '{{ prev_ds }}' AND '{{ ds }}'
                )
                SELECT * FROM cte_shipment
                """,
            "stock": """
                SELECT 
                    ss.WarehouseID,
                    ss.ProductID,
                    ss.Quantity
                FROM RETAIL_SUPPLY_CHAIN.Stock ss
                """
        }

        elt_pipeline(table_names = table_fact,
                     source_conn = database_conn,
                     snowflake_conn = snowflake_conn,
                     schema = "landing",
                     type = "fact", 
                     queries = queries
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
