from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class AzureStorageConfig:
    account_name: str
    container: str
    connection_string: str | None = None

def get_storage_config() -> AzureStorageConfig:
    account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME", "").strip()
    container = os.getenv("AZURE_STORAGE_CONTAINER", "").strip() or "bronze"
    conn = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if not account_name:
        # account_name is not strictly required if using connection string, but helpful for clarity
        account_name = "UNKNOWN_ACCOUNT"
    return AzureStorageConfig(account_name=account_name, container=container, connection_string=conn)

@dataclass(frozen=True)
class SqlConfig:
    server: str
    database: str
    username: str
    password: str

def get_sql_config() -> SqlConfig | None:
    server = os.getenv("SQL_SERVER", "").strip()
    database = os.getenv("SQL_DATABASE", "").strip()
    username = os.getenv("SQL_USERNAME", "").strip()
    password = os.getenv("SQL_PASSWORD", "").strip()
    if not (server and database and username and password):
        return None
    return SqlConfig(server=server, database=database, username=username, password=password)
