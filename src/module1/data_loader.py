import pandas as pd
import json
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "data" / "raw"

csv_files = [
    "transactions.csv",
    "customers.csv",
    "products.csv",
    "stores.csv",
    "returns.csv",
    "inventory.csv",
    "store_targets_legacy.csv"
]

data = {}

# Load CSV files
for file in csv_files:
    try:
        df = pd.read_csv(path / file)
        data[file] = df

        print(f"✓ {file}: {len(df)} rows, {len(df.columns)} columns")
        print(f"  Missing: {df.isna().sum().sum()}")
        print(f"  Duplicates: {df.duplicated().sum()}")

    except Exception as e:
        print(f"✗ Error loading {file}: {e}")

# Load JSON
try:
    with open(path / "campaigns.json", encoding="utf-8") as f:
        data["campaigns.json"] = json.load(f)

    print(f"✓ campaigns.json: {len(data['campaigns.json'])} records")

except Exception as e:
    print(f"✗ Error loading campaigns.json: {e}")

print("\n✓ Module 1 - Ingestion completed")