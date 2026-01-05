import click
from pathlib import Path
from rich import print
from azure.storage.blob import BlobServiceClient
from .config import get_storage_config

@click.command()
@click.option("--local-path", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--remote-path", required=True, help="Path inside the container, e.g. bronze/user_activity/dt=2024-01-01/file.csv")
def main(local_path: str, remote_path: str):
    cfg = get_storage_config()
    if not cfg.connection_string:
        raise SystemExit("Missing AZURE_STORAGE_CONNECTION_STRING in .env (demo). Add it or switch to AAD auth.")

    bsc = BlobServiceClient.from_connection_string(cfg.connection_string)
    container_client = bsc.get_container_client(cfg.container)

    lp = Path(local_path)
    blob_name = remote_path.lstrip("/")

    print(f"[cyan]Uploading[/cyan] {lp} -> container='{cfg.container}' blob='{blob_name}'")
    with lp.open("rb") as f:
        container_client.upload_blob(name=blob_name, data=f, overwrite=True)

    print("[green]Upload complete.[/green]")

if __name__ == "__main__":
    main()
