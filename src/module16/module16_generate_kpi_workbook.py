import pandas as pd
from pathlib import Path

# Paths
root = Path(__file__).resolve().parents[2]

input_file = root / "data/processed/module4_analysis_ready.csv"
output_file = root / "reports/week4/module16_kpi_workbook.xlsx"

# Load dataset
df = pd.read_csv(input_file)

# Clean data
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["LineAmount"] = pd.to_numeric(
    df["LineAmount"], errors="coerce"
).fillna(0)

df["Quantity"] = pd.to_numeric(
    df["Quantity"], errors="coerce"
).fillna(0)

# Remove blank IDs before counting unique values
df["TransactionID"] = df["TransactionID"].astype("string").str.strip()
df["CustomerID"] = df["CustomerID"].astype("string").str.strip()
df["ProductID"] = df["ProductID"].astype("string").str.strip()

df["TransactionID"] = df["TransactionID"].replace("", pd.NA)
df["CustomerID"] = df["CustomerID"].replace("", pd.NA)
df["ProductID"] = df["ProductID"].replace("", pd.NA)

# KPI calculations
transactions = df["TransactionID"].nunique()
total_revenue = df["LineAmount"].sum()
total_quantity = df["Quantity"].sum()

average_order_value = (
    total_revenue / transactions if transactions > 0 else 0
)

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
        round(total_revenue, 2),
        total_quantity,
        round(average_order_value, 2),
        df["CustomerID"].nunique(),
        df["ProductID"].nunique()
    ]
})

# Store summary
store = df.groupby(
    "StoreName", dropna=False
).agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Transactions=("TransactionID", "nunique")
).reset_index()

# Product summary
product = df.groupby(
    "ProductID", dropna=False
).agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Transactions=("TransactionID", "nunique")
).reset_index()

# Channel summary
channel = df.groupby(
    "Channel", dropna=False
).agg(
    Total_Revenue=("LineAmount", "sum"),
    Transactions=("TransactionID", "nunique"),
    Total_Quantity=("Quantity", "sum")
).reset_index()

# Monthly summary
monthly_df = df.dropna(subset=["OrderDate"]).copy()

monthly_df["Month"] = monthly_df["OrderDate"].dt.to_period("M")

monthly = monthly_df.groupby("Month").agg(
    Total_Revenue=("LineAmount", "sum"),
    Total_Quantity=("Quantity", "sum"),
    Transactions=("TransactionID", "nunique")
).reset_index()

monthly["Month"] = monthly["Month"].astype(str)

# Sort summaries
store = store.sort_values("Total_Revenue", ascending=False)
product = product.sort_values("Total_Revenue", ascending=False)
channel = channel.sort_values("Total_Revenue", ascending=False)
monthly = monthly.sort_values("Month")

# Create output directory
output_file.parent.mkdir(parents=True, exist_ok=True)

# Export to Excel
with pd.ExcelWriter(output_file, engine="openpyxl") as writer:

    kpis.to_excel(
        writer, sheet_name="KPI Summary", index=False
    )

    store.to_excel(
        writer, sheet_name="Store Summary", index=False
    )

    product.to_excel(
        writer, sheet_name="Product Summary", index=False
    )

    channel.to_excel(
        writer, sheet_name="Channel Summary", index=False
    )

    monthly.to_excel(
        writer, sheet_name="Monthly Summary", index=False
    )

    # Format workbook
    for sheet_name, worksheet in writer.sheets.items():

        worksheet.freeze_panes = "A2"
        worksheet.auto_filter.ref = worksheet.dimensions

        # Bold column headings
        for cell in worksheet[1]:
            cell.font = cell.font.copy(bold=True)

        # Adjust column widths
        for column_cells in worksheet.columns:
            max_length = max(
                len(str(cell.value)) if cell.value is not None else 0
                for cell in column_cells
            )

            column_letter = column_cells[0].column_letter

            worksheet.column_dimensions[column_letter].width = min(
                max_length + 3, 35
            )

    # Format KPI values
    kpi_sheet = writer.sheets["KPI Summary"]

    for row in range(2, kpi_sheet.max_row + 1):
        kpi_name = kpi_sheet.cell(row=row, column=1).value
        value_cell = kpi_sheet.cell(row=row, column=2)

        if kpi_name in ["Total Revenue", "Average Order Value"]:
            value_cell.number_format = '#,##0.00'

        elif kpi_name in [
            "Total Sales Records",
            "Total Quantity",
            "Unique Customers",
            "Unique Products"
        ]:
            value_cell.number_format = '#,##0'

print("Module 16 workbook created successfully!")
print(f"Output: {output_file}")
print("\nKPI Summary:")
print(kpis.to_string(index=False))