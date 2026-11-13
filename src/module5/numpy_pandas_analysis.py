import pandas as pd
import numpy as np
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
reports = root / "reports" / "week2"
reports.mkdir(parents=True, exist_ok=True)

# Load integrated dataset
df = pd.read_csv(data / "module4_analysis_ready.csv")

# Clean required numeric columns
for column in ["Quantity", "Discount", "LineAmount"]:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Calculated column
# LineAmount is treated as the total line value
df["Revenue"] = df["LineAmount"]

# NumPy array operations
revenue_array = df["Revenue"].dropna().to_numpy()

print("Total Revenue:", np.sum(revenue_array))
print("Mean Revenue:", np.mean(revenue_array))
print("Median Revenue:", np.median(revenue_array))
print("Standard Deviation:", np.std(revenue_array))

# Multi-level groupby
groupby_summary = (
    df.groupby(["Region", "Channel"], dropna=False)["Revenue"]
    .sum()
    .reset_index()
    .sort_values("Revenue", ascending=False)
)

groupby_summary.to_csv(
    reports / "module5_groupby_summary.csv", index=False
)

# Pivot table
pivot = pd.pivot_table(
    df,
    values="Revenue",
    index="Region",
    columns="Channel",
    aggfunc="sum",
    fill_value=0
)

pivot.to_csv(reports / "module5_pivot_table.csv")

# IQR outlier detection
revenue = df["Revenue"].dropna()

q1 = revenue.quantile(0.25)
q3 = revenue.quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = df[
    (df["Revenue"] < lower_bound) |
    (df["Revenue"] > upper_bound)
]

outliers.to_csv(reports / "module5_outliers.csv", index=False)

# Correlation analysis
correlation = df[
    ["Quantity", "Discount", "LineAmount", "Revenue"]
].corr()

correlation.to_csv(reports / "module5_correlation.csv")

# Written interpretation
highest_group = groupby_summary.iloc[0] if not groupby_summary.empty else None

with open(
    reports / "module5_interpretation.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("MODULE 5: NUMPY AND PANDAS ANALYSIS\n\n")

    file.write(f"Total Revenue: {np.sum(revenue_array):.2f}\n")
    file.write(f"Mean Revenue: {np.mean(revenue_array):.2f}\n")
    file.write(f"Median Revenue: {np.median(revenue_array):.2f}\n")
    file.write(f"Standard Deviation: {np.std(revenue_array):.2f}\n\n")

    if highest_group is not None:
        file.write(
            f"Highest revenue group: Region={highest_group['Region']}, "
            f"Channel={highest_group['Channel']}, "
            f"Revenue={highest_group['Revenue']:.2f}\n"
        )

    file.write(f"Number of IQR outliers: {len(outliers)}\n")
    file.write(f"IQR lower bound: {lower_bound:.2f}\n")
    file.write(f"IQR upper bound: {upper_bound:.2f}\n\n")

    file.write("Correlation matrix:\n")
    file.write(correlation.to_string())
    file.write("\n\nInterpretation guidance:\n")
    file.write(
        "Correlation values near +1 indicate a strong positive "
        "linear relationship; values near -1 indicate a strong "
        "negative relationship. Values near 0 indicate a weak "
        "linear relationship. Correlation does not prove causation.\n"
    )

print("\nModule 5 completed successfully!")
print("Reports saved in:", reports)