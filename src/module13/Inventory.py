import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
out = root / "reports" / "week3"
out.mkdir(parents=True, exist_ok=True)

# Load inventory data
df = pd.read_csv(data / "module3_inventory_clean.csv")

print("Inventory columns:", df.columns.tolist())

# Save inventory summary by available store and product columns
group_cols = [
    col for col in ["StoreID", "ProductID"]
    if col in df.columns
]

if not group_cols:
    raise ValueError("StoreID or ProductID column is missing.")

df.to_csv(out / "module13_inventory_analysis.csv", index=False)

# Identify stock quantity column
stock_col = next(
    (col for col in df.columns
     if any(word in col.lower() for word in
            ["stockquantity", "stock_qty", "quantity", "stocklevel", "stock"])),
    None
)

if stock_col:
    df[stock_col] = pd.to_numeric(df[stock_col], errors="coerce")

    low_stock = df[df[stock_col] <= 10]
    low_stock.to_csv(
        out / "module13_low_stock.csv", index=False
    )

    print("\nLow-stock records:", len(low_stock))
else:
    print("Stock quantity column not detected. Check the printed columns.")

print("\nModule 13 completed!")
print(f"Reports saved in: {out}")