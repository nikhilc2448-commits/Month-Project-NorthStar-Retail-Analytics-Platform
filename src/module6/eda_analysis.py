import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
reports = root / "reports" / "week2"
reports.mkdir(parents=True, exist_ok=True)

# Load integrated sales data
df = pd.read_csv(data / "module4_analysis_ready.csv")

# Prepare columns
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["LineAmount"] = pd.to_numeric(df["LineAmount"], errors="coerce")

# Revenue uses LineAmount as the total line value
df["Revenue"] = df["LineAmount"]

# Add product category
products = pd.read_csv(data / "module3_products_clean.csv")

df = df.merge(
    products[["ProductID", "Category"]],
    on="ProductID",
    how="left",
    validate="many_to_one"
)

# Create monthly period
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)

# Sales analysis by store, channel, category, region and month
group_columns = [
    "StoreName",
    "Channel",
    "Category",
    "Region",
    "Month"
]

for column in group_columns:
    result = (
        df.groupby(column, dropna=False)["Revenue"]
        .sum()
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )

    result.to_csv(
        reports / f"module6_sales_by_{column.lower()}.csv",
        index=False
    )

# Identify top revenue drivers
store_sales = df.groupby("StoreName")["Revenue"].sum().sort_values(
    ascending=False
)
channel_sales = df.groupby("Channel")["Revenue"].sum().sort_values(
    ascending=False
)
category_sales = df.groupby("Category")["Revenue"].sum().sort_values(
    ascending=False
)
region_sales = df.groupby("Region")["Revenue"].sum().sort_values(
    ascending=False
)
monthly_sales = df.groupby("Month")["Revenue"].sum().sort_values(
    ascending=False
)

# Save revenue driver summary
drivers = pd.concat(
    [
        store_sales.head(5).rename_axis("Name").reset_index().assign(
            Dimension="Store"
        ).rename(columns={"StoreName": "Name", "Revenue": "Revenue"}),
        channel_sales.head(5).rename_axis("Name").reset_index().assign(
            Dimension="Channel"
        ),
        category_sales.head(5).rename_axis("Name").reset_index().assign(
            Dimension="Category"
        ),
        region_sales.head(5).rename_axis("Name").reset_index().assign(
            Dimension="Region"
        ),
        monthly_sales.head(5).rename_axis("Name").reset_index().assign(
            Dimension="Month"
        )
    ],
    ignore_index=True
)

drivers.to_csv(
    reports / "module6_revenue_drivers.csv",
    index=False
)

# Generate written findings
with open(
    reports / "module6_findings.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("MODULE 6: EXPLORATORY DATA ANALYSIS\n\n")

    file.write(f"Total Revenue: {df['Revenue'].sum():.2f}\n\n")

    if not store_sales.empty:
        file.write(
            f"Top Store: {store_sales.index[0]} "
            f"(Revenue: {store_sales.iloc[0]:.2f})\n"
        )

    if not channel_sales.empty:
        file.write(
            f"Top Channel: {channel_sales.index[0]} "
            f"(Revenue: {channel_sales.iloc[0]:.2f})\n"
        )

    if not category_sales.empty:
        file.write(
            f"Top Category: {category_sales.index[0]} "
            f"(Revenue: {category_sales.iloc[0]:.2f})\n"
        )

    if not region_sales.empty:
        file.write(
            f"Top Region: {region_sales.index[0]} "
            f"(Revenue: {region_sales.iloc[0]:.2f})\n"
        )

    if not monthly_sales.empty:
        file.write(
            f"Best Sales Month: {monthly_sales.index[0]} "
            f"(Revenue: {monthly_sales.iloc[0]:.2f})\n"
        )

    file.write(
        "\nThese findings identify the highest-revenue groups. "
        "They describe revenue contribution and do not establish "
        "the causes of sales performance.\n"
    )

# Display results
print("\nTop 5 Stores:")
print(store_sales.head(5))

print("\nSales by Channel:")
print(channel_sales)

print("\nTop 5 Categories:")
print(category_sales.head(5))

print("\nSales by Region:")
print(region_sales)

print("\nTop 5 Months:")
print(monthly_sales.head(5))

print("\nModule 6 completed successfully!")
print("Reports saved in:", reports)