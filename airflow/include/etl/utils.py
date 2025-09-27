import logging
from pathlib import Path
from docker.types import Mount

from sqlalchemy.engine import Engine

from airflow.providers.docker.operators.docker import DockerOperator
from airflow.models import Variable

def create_table_snowflake(snowflake_conn: Engine, file_path: Path):
    """
    Execute a SQL file to create tables in Snowflake.

    This function reads an external SQL file containing one or more
    SQL statements, then executes them sequentially on Snowflake.
    Each statement should be separated by a semicolon (";").
    Useful for initializing schemas/tables before an ETL process.

    Args:
        snowflake_conn (Engine): SQLAlchemy Engine or an active connection 
            to Snowflake.
        file_path (Path): Path to the .sql file containing the DDL statements 
            to create tables.

    Returns:
        None

    Raises:
        FileNotFoundError: If the SQL file does not exist.
        Exception: If an error occurs while executing SQL statements 
            on Snowflake.

    Example:
        >>> create_table_snowflake(
        ...     snowflake_conn=engine,
        ...     file_path="sql/init_tables.sql"
        ... )
    """

    if not file_path.exists():
        raise FileNotFoundError(f"File SQL tidak ditemukan: {file_path}")

    with open(file_path, "r") as f:
        sql = f.read()

    with snowflake_conn.begin() as conn:
        for stmt in sql.split(";"):
            if stmt.strip():
                logging.info(f"[SNOWFLAKE] Eksekusi statement:\n{stmt.strip()}")
                conn.execute(stmt)

def insert_snowflake(table, conn, keys, data_iter):
    """
    Custom insert method for Pandas `to_sql` with Snowflake.

    This function is intended to be passed as the `method` argument 
    to `DataFrame.to_sql`. It builds a bulk `INSERT INTO` statement 
    for Snowflake using the provided table metadata, connection, 
    and data rows.

    Args:
        table (sqlalchemy.Table): The SQLAlchemy Table object representing 
            the target table in Snowflake.
        conn (sqlalchemy.engine.Connection): Active SQLAlchemy connection 
            to the Snowflake database.
        keys (list[str]): List of column names to be inserted.
        data_iter (Iterable[tuple]): Iterable of row tuples containing the 
            values to insert.

    Returns:
        None

    Raises:
        SQLAlchemyError: If the insert statement fails to execute.

    Example:
        >>> from sqlalchemy import create_engine
        >>> engine = create_engine("snowflake://...")
        >>> df.to_sql(
        ...     "my_table",
        ...     engine,
        ...     schema="MY_SCHEMA",
        ...     if_exists="append",
        ...     index=False,
        ...     method=insert_snowflake
        ... )
    """
    table_name = table.name
    schema_name = table.schema
    column_names = ",".join(keys)
    insert_sql = f'INSERT INTO {schema_name}.{table_name} ({column_names}) VALUES '

    rows = list(data_iter)
    if not rows:
        return

    placeholders = ",".join(["(" + ",".join(["%s"] * len(keys)) + ")" for _ in rows])

    values = []
    for row in rows:
        values.extend([v if v is not None else None for v in row])

    conn.execute(insert_sql + placeholders, values)

def make_dbt_task(task_id: str, command: list, project_path, profile_path):
    """
    Create an Airflow task using DockerOperator to execute dbt commands.

    This function wraps the configuration of `DockerOperator` to simplify
    the creation of dbt tasks within an Airflow DAG. The task will run
    a container based on the image `ghcr.io/dbt-labs/dbt-snowflake:1.9.latest`
    with predefined mounts, network, and environment settings.

    Args:
        task_id (str): Unique ID for the task within the Airflow DAG.
            Also used as the container name (prefixed with "dbt-").
        command (list): List of commands to be executed inside the dbt container.
            Example: ["run"], ["test", "--select", "model:dim_*"], etc.

    Returns:
        DockerOperator: An Airflow operator that runs a dbt container
        with the specified configuration.

    Raises:
        KeyError: If `dbt_path` does not contain the keys `profile_path` or `project_path`.
        AirflowNotFoundException: If the Airflow Variable `dbt_path` is not defined.

    Example:
        >>> dbt_run = make_dbt_task(
        ...     task_id="dbt_run",
        ...     command=["run", "--models", "stg_*"]
        ... )
    """

    return DockerOperator(
                        task_id=task_id,
                        image="ghcr.io/dbt-labs/dbt-snowflake:1.9.latest",
                        command=command,
                        container_name=f"dbt-{task_id}",
                        api_version="auto",
                        auto_remove="success",
                        docker_url="tcp://docker-proxy:2375",
                        network_mode="airflow_fb4c73_dimsnet",
                        mount_tmp_dir=False,
                        tty=False,
                        xcom_all=False,
                        mounts=[
                            Mount(
                                source=project_path,
                                target="/usr/app/dbt", 
                                type="bind"
                                ),
                                    
                            Mount(
                                source=profile_path, 
                                target="/root/.dbt", 
                                type="bind"
                                )
                            ],
                        environment={"RUN_DATE": "{{ ds }}"}
                        )
