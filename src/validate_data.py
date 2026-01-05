import click
import pandas as pd
from rich import print

REQUIRED_COLS = {"user_id","event_type","event_time","device","session_id"}

@click.command()
@click.option("--input", "input_path", required=True, type=click.Path(exists=True, dir_okay=False))
def main(input_path: str):
    df = pd.read_csv(input_path)
    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise SystemExit(f"Missing required columns: {sorted(missing)}")

    # Basic checks
    null_counts = df.isna().sum()
    dupes = df.duplicated().sum()

    print("[bold]Validation summary[/bold]")
    print(f"Rows: {len(df)}")
    print(f"Duplicate rows: {dupes}")
    print("Null counts:")
    print(null_counts)

    # Assert at least some non-null in key columns
    for c in ["user_id","event_type","event_time"]:
        if df[c].isna().all():
            raise SystemExit(f"Column {c} is entirely null.")

    print("[green]Validation OK.[/green]")

if __name__ == "__main__":
    main()
