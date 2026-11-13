import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
input_file = root / "data/processed/module4_analysis_ready.csv"
output_file = root / "reports/week4/module16_kpi_workbook.xlsx"

df = pd.read_csv(input_file)

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["LineAmount"] = pd.to_numeric(df["LineAmount"], errors="coerce").fillna(0)
df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce").fillna(0)

transactions = df["TransactionID"].nunique()

kpis = pd.DataFrame({
    "KPI": [
        "Total Sales Records",
        "Total Revenue",
        "Total Quantity",
        "Average Order Value",
        "Unique Customers",
        "Unique Products"
    ],
    "Value": [
        transactions,
        df["LineAmount"].sum(),
        df["Quantity"].sum(),
        df["LineAmount"].sum() / max(transactions, 1),
        df.loc[df["CustomerID"].notna(), "CustomerID"].nunique(),
        df["ProductID"].nunique()
    ]
})

store = df.groupby("StoreName", dropna=False).agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Transactions=("TransactionID", "nunique")
).reset_index()

product = df.groupby("ProductID", dropna=False).agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

channel = df.groupby("Channel", dropna=False).agg(
    Total_Revenue=("LineAmount", "sum"),
    Transactions=("TransactionID", "nunique")
).reset_index()

monthly = df.dropna(subset=["OrderDate"]).groupby(
    df["OrderDate"].dt.to_period("M")
).agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

monthly["OrderDate"] = monthly["OrderDate"].astype(str)

output_file.parent.mkdir(parents=True, exist_ok=True)

with pd.ExcelWriter(output_file, engine="openpyxl") as writer:
    kpis.to_excel(writer, sheet_name="KPI Summary", index=False)
    store.to_excel(writer, sheet_name="Store Summary", index=False)
    product.to_excel(writer, sheet_name="Product Summary", index=False)
    channel.to_excel(writer, sheet_name="Channel Summary", index=False)
    monthly.to_excel(writer, sheet_name="Monthly Summary", index=False)

print(f"Workbook created successfully: {output_file}")



