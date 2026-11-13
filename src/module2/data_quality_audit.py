import pandas as pd
import json
from pathlib import Path

path = Path(__file__).resolve().parents[2] / "data" / "raw"
report = Path(__file__).resolve().parents[2] / "reports" / "week1"
report.mkdir(parents=True, exist_ok=True)

files = [
    "transactions.csv", "customers.csv", "products.csv",
    "stores.csv", "returns.csv", "inventory.csv",
    "store_targets_legacy.csv"
]

summary = []
columns = []

# CSV audit
for file in files:
    df = pd.read_csv(path / file)

    summary.append({
        "file": file,
        "rows": len(df),
        "columns": len(df.columns),
        "missing": df.isna().sum().sum(),
        "duplicates": df.duplicated().sum()
    })

    for col in df.columns:
        columns.append({
            "file": file,
            "column": col,
            "dtype": str(df[col].dtype),
            "missing": df[col].isna().sum(),
            "unique": df[col].nunique()
        })

# JSON audit
with open(path / "campaigns.json", encoding="utf-8") as f:
    campaigns = json.load(f)

summary.append({
    "file": "campaigns.json",
    "rows": len(campaigns),
    "columns": len(campaigns[0]) if campaigns else 0,
    "missing": pd.json_normalize(campaigns).isna().sum().sum(),
    "duplicates": pd.json_normalize(campaigns).duplicated().sum()
})

# Save audit reports
pd.DataFrame(summary).to_csv(
    report / "module2_data_quality_summary.csv", index=False
)

pd.DataFrame(columns).to_csv(
    report / "module2_column_quality_audit.csv", index=False
)

print("✓ Data quality audit completed")
print("✓ Reports saved in reports/week1/")