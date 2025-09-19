import logging
import tomllib
from pathlib import Path

from sqlalchemy import create_engine
from airflow.exceptions import AirflowFailException


def get_snowflake_conn(file_path: str, pool_size: int = 2, max_overflow: int = 2, pool_timeout: int = 60, pool_recycle: int = 6000, pool_pre_ping: bool = True):
    """
    Create a SQLAlchemy Engine for Snowflake.

    This function reads Snowflake credentials from a `.secrets.toml` file 
    and initializes a SQLAlchemy engine with connection pooling settings.

    Args:
        file_path (Path): Path to the `.secrets.toml` file containing Snowflake credentials.
        pool_size (int, optional): Maximum number of persistent connections in the pool. Default is 2.
        max_overflow (int, optional): Maximum number of temporary overflow connections. Default is 2.
        pool_timeout (int, optional): Timeout (in seconds) when waiting for a connection before raising an error. Default is 60.
        pool_recycle (int, optional): Maximum lifetime (in seconds) of a connection before recycling. Default is 6000.
        pool_pre_ping (bool, optional): Whether to test connections before using them. Default is True.

    Returns:
        sqlalchemy.engine.base.Engine: A SQLAlchemy Engine configured for Snowflake.

    Raises:
        FileNotFoundError: If the `.secrets.toml` file does not exist.
        AirflowFailException: If the connection to Snowflake cannot be established.

    Example:
        >>> engine = get_snowflake_conn(Path("/opt/config/.secrets.toml"))
        >>> pd.read_sql("SELECT CURRENT_TIMESTAMP()", con=engine)
    """

    if not file_path.exists():
        raise FileNotFoundError(f"Secrets file tidak ditemukan: {file_path}")

    with open(file_path, "rb") as f:
        secrets = tomllib.load(f)

    secrets_sf = secrets["snowflake"]

    user = secrets_sf["user"]
    password = secrets_sf["password"]
    account = secrets_sf["account"]
    warehouse = secrets_sf["warehouse"]
    schema = secrets_sf["schema"]
    database = secrets_sf["database"]
    role = secrets_sf["role"]

    uri = f"snowflake://{user}:{password}@{account}/{database}/{schema}?warehouse={warehouse}&role={role}"

    try:    
        logging.info("[SNOWFLAKE] Koneksi berhasil dibuat.")
        return create_engine(
                            uri,
                            pool_size = pool_size,
                            max_overflow = max_overflow,
                            pool_timeout = pool_timeout,
                            pool_recycle = pool_recycle,
                            pool_pre_ping = pool_pre_ping
                            )
    except Exception as e:
        raise AirflowFailException(f"Gagal konek ke Snowflake: {e}")

def get_database_conn(file_path: str, conn_type: str, pool_size: int = 2, max_overflow: int = 2, pool_timeout: int = 60, pool_recycle: int = 6000, pool_pre_ping: bool = True):
    """
    Create a SQLAlchemy Engine for MySQL or PostgreSQL.

    This function reads database credentials from a `.secrets.toml` file 
    and initializes a SQLAlchemy engine with connection pooling settings.

    Args:
        file_path (Path): Path to the `.secrets.toml` file containing database credentials.
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
    if not file_path.exists():
        raise FileNotFoundError(f"Secrets file tidak ditemukan: {file_path}")

    with open(file_path, "rb") as f:
        secrets = tomllib.load(f)

    secrets_db = secrets[conn_type]

    user = secrets_db["user"]
    password = secrets_db["password"]
    host = secrets_db["host"]
    port = secrets_db["port"]
    database = secrets_db["database"]

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