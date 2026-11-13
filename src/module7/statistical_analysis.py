import pandas as pd
import numpy as np
from pathlib import Path
from scipy.stats import ttest_ind

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
reports = root / "reports" / "week2"
reports.mkdir(parents=True, exist_ok=True)

# Load transactions and returns
transactions = pd.read_csv(data / "module4_analysis_ready.csv")
returns = pd.read_csv(data / "module3_returns_clean.csv")

# Convert numeric columns
for col in ["Quantity", "Discount", "LineAmount"]:
    transactions[col] = pd.to_numeric(
        transactions[col], errors="coerce"
    )

# Descriptive statistics
stats = transactions[
    ["Quantity", "Discount", "LineAmount"]
].describe()

stats.to_csv(reports / "module7_descriptive_statistics.csv")

# Random sampling
sample = transactions.sample(
    n=min(1000, len(transactions)),
    random_state=42
)

sample.to_csv(reports / "module7_random_sample.csv", index=False)

# Identify return records
# Adjust these column names if your dataset uses different names.
print("Transaction columns:", transactions.columns.tolist())
print("Return columns:", returns.columns.tolist())

# Match returned transactions using OrderID
# Match returned transactions using TransactionID
returned_ids = returns["TransactionID"].dropna().unique()

transactions["Returned"] = (
    transactions["TransactionID"].isin(returned_ids)
)

# Function to perform hypothesis tests
def test_hypothesis(column, label):
    returned = transactions.loc[
        transactions["Returned"], column
    ].dropna()

    not_returned = transactions.loc[
        ~transactions["Returned"], column
    ].dropna()

    if len(returned) < 2 or len(not_returned) < 2:
        return {
            "Metric": label,
            "Returned_Mean": returned.mean(),
            "Not_Returned_Mean": not_returned.mean(),
            "P_Value": np.nan,
            "Result": "Insufficient data"
        }

    # Welch's independent-samples t-test
    statistic, p_value = ttest_ind(
        returned,
        not_returned,
        equal_var=False
    )

    result = (
        "Statistically significant difference"
        if p_value < 0.05
        else "No statistically significant difference"
    )

    return {
        "Metric": label,
        "Returned_Mean": returned.mean(),
        "Not_Returned_Mean": not_returned.mean(),
        "P_Value": p_value,
        "Result": result
    }

# Test two business hypotheses
results = pd.DataFrame([
    test_hypothesis("Discount", "Discount"),
    test_hypothesis("Quantity", "Quantity")
])

results.to_csv(
    reports / "module7_hypothesis_tests.csv",
    index=False
)

# Save interpretation
with open(
    reports / "module7_interpretation.txt",
    "w",
    encoding="utf-8"
) as file:
    file.write("MODULE 7: STATISTICAL ANALYSIS\n\n")
    file.write(f"Transaction count: {len(transactions)}\n")
    file.write(f"Sample size: {len(sample)}\n\n")

    file.write("Hypothesis test results:\n")
    file.write(results.to_string(index=False))
    file.write("\n\nSignificance level: 0.05\n")
    file.write(
        "A p-value below 0.05 indicates evidence of a difference "
        "between returned and non-returned transactions. "
        "This does not prove causation.\n"
    )

print("\nModule 7 completed!")
print(results)
print("\nReports saved in:", reports)