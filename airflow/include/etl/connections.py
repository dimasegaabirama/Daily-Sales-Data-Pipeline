import json
import logging
from pathlib import Path

from sqlalchemy import create_engine
from airflow.exceptions import AirflowFailException
from airflow.hooks.base import BaseHook


def get_snowflake_conn(
    connection_name: str,
    pool_size: int = 2,
    max_overflow: int = 2,
    pool_timeout: int = 60,
    pool_recycle: int = 6000,
    pool_pre_ping: bool = True,
):
    """
    Create a SQLAlchemy Engine for Snowflake using Airflow Connection.

    This function retrieves Snowflake credentials from an Airflow Connection
    (configured in the Airflow UI or via YAML import) and initializes a 
    SQLAlchemy engine with connection pooling settings.

    Args:
        connection_name (str): The Airflow connection ID for Snowflake.
        pool_size (int, optional): Maximum number of persistent connections in the pool. Default is 2.
        max_overflow (int, optional): Maximum number of temporary overflow connections. Default is 2.
        pool_timeout (int, optional): Timeout (in seconds) when waiting for a connection before raising an error. Default is 60.
        pool_recycle (int, optional): Maximum lifetime (in seconds) of a connection before recycling. Default is 6000.
        pool_pre_ping (bool, optional): Whether to test connections before using them. Default is True.

    Returns:
        sqlalchemy.engine.base.Engine: A SQLAlchemy Engine configured for Snowflake.

    Raises:
        AirflowFailException: If the connection to Snowflake cannot be established.

    Example:
        >>> engine = get_snowflake_conn("snowflake_conn")
        >>> pd.read_sql("SELECT CURRENT_TIMESTAMP()", con=engine)
    """
    try:
        conn = BaseHook.get_connection(connection_name)
        conn_extra = json.loads(conn.extra or "{}")

        user = conn.login
        password = conn.password
        database = conn.schema
        account = conn_extra.get("account")
        warehouse = conn_extra.get("warehouse")
        schema = conn_extra.get("schema")
        role = conn_extra.get("role")

        uri = (
            f"snowflake://{user}:{password}@{account}/{database}/{schema}"
            f"?warehouse={warehouse}&role={role}"
        )

        logging.info(
            "[SNOWFLAKE] Membuat koneksi ke account=%s, database=%s, schema=%s, warehouse=%s",
            account,
            database,
            schema,
            warehouse,
        )

        return create_engine(
            uri,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_timeout=pool_timeout,
            pool_recycle=pool_recycle,
            pool_pre_ping=pool_pre_ping,
        )

    except Exception as e:
        logging.error("[SNOWFLAKE] Gagal koneksi: %s", str(e))
        raise AirflowFailException(f"Gagal konek ke Snowflake: {e}")

def get_database_conn(
    connection_name: str, 
    conn_type: str, 
    pool_size: int = 2, 
    max_overflow: int = 2, 
    pool_timeout: int = 60, 
    pool_recycle: int = 6000, 
    pool_pre_ping: bool = True
):
    """
    Create a SQLAlchemy Engine for MySQL or PostgreSQL.

    This function reads database credentials from a `.secrets.toml` file 
    and initializes a SQLAlchemy engine with connection pooling settings.

    Args:
        connection_name (str): The Airflow connection ID for Database.
        conn_type (str): Database type, must be either "mysql" or "postgres".
        pool_size (int, optional): Maximum number of persistent connections in the pool. Default is 2.
        max_overflow (int, optional): Maximum number of temporary overflow connections. Default is 2.
        pool_timeout (int, optional): Timeout (in seconds) when waiting for a connection before raising an error. Default is 60.
        pool_recycle (int, optional): Maximum lifetime (in seconds) of a connection before recycling. Default is 6000.
        pool_pre_ping (bool, optional): Whether to test connections before using them. Default is True.

    Returns:
        sqlalchemy.engine.base.Engine: A SQLAlchemy Engine configured for the specified database.

    Raises:
        FileNotFoundError: If the `.secrets.toml` file does not exist.
        AirflowFailException: If the database type is unsupported or the connection fails.

    Example:
        >>> engine = get_database_conn(Path("/opt/config/.secrets.toml"), conn_type="mysql")
        >>> pd.read_sql("SELECT NOW()", con=engine)

        >>> engine = get_database_conn(Path("/opt/config/.secrets.toml"), conn_type="postgres")
        >>> pd.read_sql("SELECT current_date", con=engine)
    """
    conn = BaseHook.get_connection(connection_name)

    user = conn.login
    password = conn.password
    host = conn.host
    port = conn.port
    database = conn.schema

    if conn_type == "mysql":
        uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    elif conn_type == "postgres":
        uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    else:
        raise AirflowFailException(f"Tipe connection {conn_type} belum didukung")

    try:    
        logging.info("[DATABASE] Koneksi berhasil dibuat.")
        return create_engine(
                            uri,
                            pool_size = pool_size,
                            max_overflow = max_overflow,
                            pool_timeout = pool_timeout,
                            pool_recycle = pool_recycle,
                            pool_pre_ping = pool_pre_ping
                            )
    except Exception as e:
        raise AirflowFailException(f"Gagal konek ke {conn_type}: {e}")

if __name__ == "__main__":
    pass