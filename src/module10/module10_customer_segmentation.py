import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
out = root / "reports" / "week3"
out.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(data / "module4_analysis_ready.csv")

df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["LineAmount"] = pd.to_numeric(df["LineAmount"], errors="coerce")

df = df.dropna(
    subset=["CustomerID", "TransactionID", "OrderDate", "LineAmount"]
)

df = df[
    ~df["CustomerID"].astype(str).isin(["Unknown", "", "nan", "None"])
]

reference_date = df["OrderDate"].max().normalize() + pd.Timedelta(days=1)

# Calculate RFM metrics
rfm = df.groupby("CustomerID").agg(
    Recency=("OrderDate", lambda x: (reference_date - x.max().normalize()).days),
    Frequency=("TransactionID", "nunique"),
    Monetary=("LineAmount", "sum")
).reset_index()

# Assign scores from 1 to 5
for col, higher_is_better in [
    ("Recency", False),
    ("Frequency", True),
    ("Monetary", True)
]:
    ranks = rfm[col].rank(method="first")
    scores = pd.qcut(ranks, 5, labels=[1, 2, 3, 4, 5]).astype(int)
    rfm[f"{col[0]}_Score"] = scores if higher_is_better else 6 - scores

rfm["RFM_Total"] = rfm[["R_Score", "F_Score", "M_Score"]].sum(axis=1)

# Segment customers
def segment(row):
    r, f, m = row["R_Score"], row["F_Score"], row["M_Score"]

    if r >= 4 and f >= 4 and m >= 4:
        return "Champions"
    elif r >= 3 and f >= 4:
        return "Loyal Customers"
    elif r <= 2 and f >= 3 and m >= 3:
        return "At Risk"
    elif r <= 2 and f <= 2:
        return "Inactive Customers"
    else:
        return "Regular Customers"

rfm["CustomerSegment"] = rfm.apply(segment, axis=1)

# Save customer segments
rfm.to_csv(out / "module10_customer_segments.csv", index=False)

# Segment summary
summary = rfm.groupby("CustomerSegment").agg(
    CustomerCount=("CustomerID", "nunique"),
    AverageRecency=("Recency", "mean"),
    AverageFrequency=("Frequency", "mean"),
    AverageSpending=("Monetary", "mean"),
    TotalRevenue=("Monetary", "sum")
).reset_index()

summary.to_csv(out / "module10_segment_summary.csv", index=False)

print("Module 10 completed!")
print(summary)
print(f"Reports saved in: {out}")