import logging
from pathlib import Path

from sqlalchemy.engine import Engine

from .extract import extract_from_source
from .load import load_to_snowflake
from .utils import insert_snowflake


def elt_pipeline(
    path_file: Path,
    source_conn: Engine,
    snowflake_conn: Engine,
    prev_ds = None,
    ds = None,
    schema: str = "RAW",
    type: str = "dimension"
):
    """
    Run a simple ELT pipeline from a source database to Snowflake.

    Depending on the table type ("dimension" or "fact"), this function 
    extracts data from the source, transforms it if necessary (via custom 
    queries for fact tables), and then loads it into Snowflake. 

    - For **dimension tables**: if a SQL file is empty, data is extracted 
      directly from the source table. If it contains a query, that query is 
      used for extraction.
    - For **fact tables**: a SQL query must be provided in the `.sql` file. 
      The query can include placeholders `{prev_ds}` and `{ds}` which will 
      be substituted.

    Args:
        path_file (Path): Path directory containing `.sql` files.
        source_conn (Engine): SQLAlchemy Engine or active connection 
            to the source database.
        snowflake_conn (Engine): SQLAlchemy Engine or active connection 
            to Snowflake.
        schema (str, optional): Target Snowflake schema. Defaults to `"RAW"`.
        type (str, optional): Table type, must be `"dimension"` or `"fact"`. 
            Defaults to `"dimension"`.

    Returns:
        None
    """
    
    sql_files = list(path_file.glob("*.sql"))

    if type == "dimension":
        for sql_file in sql_files:
            table_name = sql_file.stem
            sql_text = sql_file.read_text().strip()

            if not sql_text:
                df = extract_from_source(table_name, source_conn)
            else:
                df = extract_from_source(table_name, source_conn, query=sql_text)

            load_to_snowflake(
                df=df,
                conn_snowflake=snowflake_conn,
                table_name=table_name,
                schema=schema,
                method=insert_snowflake,
            )

    elif type == "fact":
        for sql_file in sql_files:
            table_name = sql_file.stem
            sql_text = sql_file.read_text().strip()

            if not sql_text:
                raise ValueError(f"Query kosong di file {sql_file}")

            # Replace placeholders (Airflow-style macros bisa masuk di sini)
            formatted_sql = sql_text.format(prev_ds=prev_ds, ds=ds)

            df = extract_from_source(table_name, source_conn, query=formatted_sql)

            load_to_snowflake(
                df=df,
                conn_snowflake=snowflake_conn,
                table_name=table_name,
                schema=schema,
                method=insert_snowflake,
            )

    else:
        raise ValueError("type harus 'dimension' atau 'fact'")
