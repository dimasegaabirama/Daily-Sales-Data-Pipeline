import logging
from typing import Callable, Optional, Union

import pandas as pd
from sqlalchemy.engine import Engine
from airflow.exceptions import AirflowFailException

def load_to_snowflake(
    df: pd.DataFrame,
    conn_snowflake: Engine,
    table_name: str,
    schema: str = "LANDING",
    chunksize: Optional[int] = None,
    if_exists: str = "append",
    method: Optional[Union[str, Callable]] = None
):
    """
    Load data from a Pandas DataFrame into a Snowflake table.

    This function leverages Pandas `to_sql()` via SQLAlchemy to insert data
    into Snowflake. The operation is wrapped in a transaction: if any error
    occurs, all changes will be rolled back.

    Args:
        df (pd.DataFrame): DataFrame containing the data to load.
        conn_snowflake (Engine): SQLAlchemy Engine or active connection 
            to Snowflake.
        table_name (str): Name of the target table in Snowflake.
        schema (str, optional): Snowflake schema where the table resides. 
            Defaults to `"LANDING"`.
        chunksize (int, optional): Number of rows per batch insert. 
            - None: write all rows at once.
            - int: split inserts into batches of this size.
        if_exists (str, optional): Behavior if the target table already exists:
            - "fail"    : Raise an error.
            - "replace" : Drop the existing table, recreate it, and load data.
            - "append"  : Insert new rows into the existing table.
            Defaults to `"append"`.
        method (str or Callable, optional): Insert method passed to Pandas `to_sql`.
            - None: Default row-by-row insert.
            - "multi": Execute batch inserts (faster).
            - Callable: Custom insert function with the signature 
              `(table, conn, keys, data_iter)`.

    Returns:
        None

    Raises:
        AirflowFailException: If the load operation into Snowflake fails.

    Example:
        >>> load_to_snowflake(
        ...     df=df,
        ...     conn_snowflake=snowflake_engine,
        ...     table_name="customers",
        ...     schema="RAW",
        ...     chunksize=100_000,
        ...     if_exists="append",
        ...     method="multi"
        ... )
    """

    try:
        with conn_snowflake.begin() as conn:
            conn.execute(f"TRUNCATE TABLE {schema}.{table_name}")
            df.to_sql(
                name=table_name,
                con=conn,
                schema=schema,
                chunksize=chunksize,
                index=False,
                if_exists=if_exists,
                method=method
            )
        row_count = len(df)
        logging.info(f"[LOAD] Table={schema}.{table_name}, STATUS=Success, ROWS={row_count}, CHUNKS={chunksize}")
    
    except Exception as e:
        raise AirflowFailException(f"[LOAD ERROR] {table_name}: {e}")

if __name__ == "__main__":
    pass