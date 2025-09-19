import logging
from typing import List

from sqlalchemy.engine import Engine

from .extract import extract_from_source
from .load import load_to_snowflake
from .utils import insert_snowflake

def elt_pipeline(
    table_names: List[str],
    source_conn: Engine,
    snowflake_conn: Engine,
    schema: str = "RAW",
    type: str = "dimension",
    queries: dict = None,
):
    
    """
    Run a simple ELT pipeline from a source database to Snowflake.

    Depending on the table type ("dimension" or "fact"), this function 
    extracts data from the source, transforms it if necessary (via custom 
    queries for fact tables), and then loads it into Snowflake. 

    - For **dimension tables**: data is extracted directly from the source 
      and loaded into Snowflake.
    - For **fact tables**: a custom SQL query must be provided via `queries`. 
      The query is executed to extract the data before loading it into Snowflake.

    Args:
        table_names (List[str]): List of table names to process.
        source_conn (Engine): SQLAlchemy Engine or active connection 
            to the source database.
        snowflake_conn (Engine): SQLAlchemy Engine or active connection 
            to Snowflake.
        schema (str, optional): Target Snowflake schema. Defaults to `"RAW"`.
        type (str, optional): Table type, must be `"dimension"` or `"fact"`. 
            Defaults to `"dimension"`.
        queries (dict, optional): A dictionary of {table_name: sql_query} 
            required when `type="fact"`.

    Returns:
        None

    Raises:
        ValueError: 
            - If `type` is not `"dimension"` or `"fact"`.
            - If `type="fact"` but no query is provided for the given table.

    Example:
        >>> elt_pipeline(
        ...     table_names=["customers", "products"],
        ...     source_conn=postgres_engine,
        ...     snowflake_conn=snowflake_engine,
        ...     schema="RAW",
        ...     type="dimension"
        ... )
        
        >>> elt_pipeline(
        ...     table_names=["sales"],
        ...     source_conn=postgres_engine,
        ...     snowflake_conn=snowflake_engine,
        ...     schema="RAW",
        ...     type="fact",
        ...     queries={"sales": "SELECT * FROM staging.sales WHERE order_date >= CURRENT_DATE - 30"}
        ... )
    """
        
    for table in table_names:
        if type == "dimension":
            df = extract_from_source(table, source_conn)

            load_to_snowflake(
                    df=df,
                    conn_snowflake=snowflake_conn, 
                    table_name=table, 
                    schema=schema, 
                    method=insert_snowflake
            )

        elif type == "fact":
            if queries is None or table not in queries:
                raise ValueError(f"Tabel fact {table} belum ada query-nya.")

            query = queries[table]
            df = extract_from_source(table, source_conn, query=query)

            load_to_snowflake(
                df=df,
                conn_snowflake=snowflake_conn,
                table_name=table,
                schema=schema,
                chunksize=100_000,
                method=insert_snowflake
            )

        else:
            raise ValueError("type harus 'dimension' atau 'fact'")
