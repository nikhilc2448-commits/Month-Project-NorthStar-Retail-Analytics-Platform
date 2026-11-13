import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"

transactions = pd.read_csv(data / "module3_transactions_clean.csv")
stores = pd.read_csv(data / "module3_stores_clean.csv")
targets = pd.read_csv(data / "module3_store_targets_legacy_clean.csv")

# Create matching month
transactions["period"] = pd.to_datetime(
    transactions["OrderDate"]
).dt.strftime("%b-%Y")

# Rename legacy key
targets = targets.rename(columns={"store_code": "StoreID"})

# Add store information
transactions = transactions.merge(
    stores[[
        "StoreID", "StoreName", "City",
        "State", "Format", "Region"
    ]],
    on="StoreID",
    how="left"
)

# Add correct monthly store targets
transactions = transactions.merge(
    targets,
    on=["StoreID", "period"],
    how="left"
)

# Remove helper column
transactions.drop(columns="period", inplace=True)

# Save
transactions.to_csv(
    data / "module4_analysis_ready.csv",
    index=False
)

print("✓ Store targets reconciled")
print(f"✓ Analysis-ready rows: {len(transactions)}")
print(f"✓ Analysis-ready columns: {len(transactions.columns)}")
print(f"✓ Saved: module4_analysis_ready.csv")
