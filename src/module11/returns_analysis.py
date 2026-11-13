import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
out = root / "reports" / "week3"
out.mkdir(parents=True, exist_ok=True)

# Load data
returns = pd.read_csv(data / "module3_returns_clean.csv")
transactions = pd.read_csv(data / "module4_analysis_ready.csv")

returns["RefundAmount"] = pd.to_numeric(
    returns["RefundAmount"], errors="coerce"
)

# Returns by reason
reason_summary = returns.groupby("Reason").agg(
    ReturnCount=("ReturnID", "count"),
    TotalRefund=("RefundAmount", "sum")
).reset_index()

reason_summary.to_csv(
    out / "module11_returns_by_reason.csv", index=False
)

# Returns by condition
condition_summary = returns.groupby("Condition").agg(
    ReturnCount=("ReturnID", "count"),
    TotalRefund=("RefundAmount", "sum")
).reset_index()

condition_summary.to_csv(
    out / "module11_returns_by_condition.csv", index=False
)

# Match returns with transactions
merged = returns.merge(
    transactions[["TransactionID", "ProductID", "StoreName", "Region"]],
    on="TransactionID",
    how="left"
)

# Returns by product
product_summary = merged.groupby("ProductID").agg(
    ReturnCount=("ReturnID", "count"),
    TotalRefund=("RefundAmount", "sum")
).reset_index()

product_summary.to_csv(
    out / "module11_returns_by_product.csv", index=False
)

# Overall summary
with open(out / "module11_findings.txt", "w", encoding="utf-8") as f:
    f.write(f"Total return records: {len(returns)}\n")
    f.write(f"Total refunds: {returns['RefundAmount'].sum():.2f}\n")
    f.write(f"Average refund: {returns['RefundAmount'].mean():.2f}\n")

print("Module 11 completed!")
print("\nReturns by reason:")
print(reason_summary)
print(f"\nReports saved in: {out}")