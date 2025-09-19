import logging

import pandas as pd
from sqlalchemy.engine import Engine
from airflow.exceptions import AirflowFailException

def extract_from_source(table_name: str, source_conn: Engine, query: str = None) -> pd.DataFrame:
    """
    Extract data from a source database into a Pandas DataFrame.

    This function retrieves data either from a given table or from a 
    custom SQL query, and returns the result as a DataFrame. It is used 
    for the "Extract" step in an ETL/ELT pipeline. If the query fails, 
    the function raises an AirflowFailException to clearly mark the DAG 
    as failed.

    Args:
        table_name (str): Name of the source table to extract from.
        source_conn (Engine or Connection): SQLAlchemy Engine or another 
            connection object compatible with `pandas.read_sql`.
        query (str, optional): Custom SQL query to extract data. 
            If None, the function automatically runs 
            `"SELECT * FROM {table_name}"`.

    Returns:
        pd.DataFrame: A DataFrame containing the extracted data.

    Raises:
        AirflowFailException: If an error occurs while executing the query.

    Example:
        >>> df = extract_from_source(
        ...     table_name="customers",
        ...     source_conn=postgres_engine
        ... )
        
        >>> df = extract_from_source(
        ...     table_name="sales",
        ...     source_conn=postgres_engine,
        ...     query="SELECT id, amount FROM sales WHERE amount > 1000"
        ... )
    """

    if query is None:
        query = f"SELECT * FROM {table_name}"

    try:
        df = pd.read_sql(sql=query, con=source_conn)
        logging.info(f"[EXTRACT] Table={table_name}, Rows={len(df)}")
        return df
    except Exception as e:
        raise AirflowFailException(f"[EXTRACT ERROR] {table_name}: {e}")

if __name__ == "__main__":
    pass