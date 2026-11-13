import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
reports = root / "reports" / "week2"
reports.mkdir(parents=True, exist_ok=True)

# Load transaction data
df = pd.read_csv(data / "module4_analysis_ready.csv")

# Validate required columns
required = ["CustomerID", "OrderDate"]

missing = [col for col in required if col not in df.columns]

if missing:
    raise ValueError(f"Missing required columns: {missing}")

# Prepare data
df["OrderDate"] = pd.to_datetime(
    df["OrderDate"], errors="coerce"
)

df = df.dropna(subset=["CustomerID", "OrderDate"])

# Exclude placeholder customer IDs if present
df = df[
    ~df["CustomerID"].astype(str).str.strip().isin(
        ["Unknown", "", "nan", "None"]
    )
]

# Use unique customer-order combinations to avoid counting
# multiple product lines from one order as multiple purchases.
if "OrderID" in df.columns:
    purchases = df[
        ["CustomerID", "OrderID", "OrderDate"]
    ].drop_duplicates()
else:
    # Fallback: use customer and transaction date.
    purchases = df[
        ["CustomerID", "OrderDate"]
    ].drop_duplicates()

# Customer cohort = month of first purchase
first_purchase = purchases.groupby(
    "CustomerID"
)["OrderDate"].min()

cohort = first_purchase.dt.to_period("M")

purchases = purchases.copy()
purchases["OrderMonth"] = (
    purchases["OrderDate"].dt.to_period("M")
)

purchases["CohortMonth"] = purchases["CustomerID"].map(cohort)

# Calculate months since cohort
purchases["CohortIndex"] = (
    (purchases["OrderMonth"].dt.year -
     purchases["CohortMonth"].dt.year) * 12
    + purchases["OrderMonth"].dt.month
    - purchases["CohortMonth"].dt.month
    + 1
)

# Count distinct active customers in each cohort/month
cohort_data = purchases.groupby(
    ["CohortMonth", "CohortIndex"]
)["CustomerID"].nunique().reset_index()

cohort_data.rename(
    columns={"CustomerID": "ActiveCustomers"},
    inplace=True
)

cohort_data.to_csv(
    reports / "module8_cohort_activity.csv",
    index=False
)

# Cohort retention table
retention = cohort_data.pivot(
    index="CohortMonth",
    columns="CohortIndex",
    values="ActiveCustomers"
)

retention.index = retention.index.astype(str)
retention.columns.name = "MonthsSinceFirstPurchase"

# Convert counts to retention percentages
cohort_sizes = retention.iloc[:, 0]
retention_percent = retention.div(cohort_sizes, axis=0) * 100

retention.to_csv(
    reports / "module8_cohort_customer_counts.csv"
)

retention_percent.to_csv(
    reports / "module8_cohort_retention.csv"
)

# Repeat-purchase behaviour
purchase_counts = purchases.groupby(
    "CustomerID"
).size()

customer_summary = pd.DataFrame({
    "PurchaseCount": purchase_counts,
    "CohortMonth": cohort
})

customer_summary["RepeatCustomer"] = (
    customer_summary["PurchaseCount"] > 1
)

customer_summary.to_csv(
    reports / "module8_customer_purchase_summary.csv"
)

repeat_rate = (
    customer_summary["RepeatCustomer"].mean() * 100
    if not customer_summary.empty else 0
)

# Summary report
with open(
    reports / "module8_retention_summary.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("MODULE 8: COHORT AND RETENTION ANALYSIS\n\n")
    file.write(f"Unique customers: {len(customer_summary)}\n")
    file.write(f"Repeat customers: {customer_summary['RepeatCustomer'].sum()}\n")
    file.write(f"Repeat customer rate: {repeat_rate:.2f}%\n\n")
    file.write(
        "Cohort month is based on each customer's first recorded purchase. "
        "Retention is the percentage of customers from each cohort who "
        "made purchases in subsequent months.\n"
    )

print("\nModule 8 completed!")
print(f"Unique customers: {len(customer_summary)}")
print(f"Repeat customer rate: {repeat_rate:.2f}%")
print("\nReports saved in:", reports)