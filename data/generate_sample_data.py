import argparse
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

EVENT_TYPES = ["login", "click", "view", "purchase", "logout"]
DEVICES = ["mobile", "web", "tablet"]

def rand_session_id() -> str:
    alphabet = "abcdef0123456789"
    return "".join(random.choice(alphabet) for _ in range(16))

def generate_rows(n: int):
    now = datetime.utcnow()
    start = now - timedelta(days=30)
    for _ in range(n):
        user_id = random.randint(1, 2000)
        event_time = start + timedelta(seconds=random.randint(0, 30 * 24 * 3600))
        yield {
            "user_id": user_id,
            "event_type": random.choice(EVENT_TYPES),
            "event_time": event_time.strftime("%Y-%m-%d %H:%M:%S"),
            "device": random.choice(DEVICES),
            "session_id": rand_session_id(),
        }

def write_csv(rows, path: Path):
    import csv
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["user_id","event_type","event_time","device","session_id"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

def write_jsonl(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=1000)
    args = parser.parse_args()

    rows = list(generate_rows(args.rows))
    write_csv(rows, Path("data/sample_events.csv"))
    write_jsonl(rows, Path("data/sample_events.jsonl"))
    print(f"Generated {args.rows} rows to data/sample_events.csv and data/sample_events.jsonl")

if __name__ == "__main__":
    main()
