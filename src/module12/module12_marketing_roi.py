import pandas as pd
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
raw = root / "data" / "raw"
processed = root / "data" / "processed"
out = root / "reports" / "week3"
out.mkdir(parents=True, exist_ok=True)

# Load campaign data
with open(raw / "campaigns.json", encoding="utf-8") as f:
    campaigns = json.load(f)

campaigns = pd.json_normalize(campaigns)

# Load transactions
transactions = pd.read_csv(
    processed / "module4_analysis_ready.csv"
)

# Save campaign data for inspection
campaigns.to_csv(
    out / "module12_campaign_data.csv", index=False
)

# Check campaign columns
print("Campaign columns:", campaigns.columns.tolist())
print("Transaction columns:", transactions.columns.tolist())

# Identify possible campaign and cost columns
campaign_cols = [
    c for c in campaigns.columns
    if "campaign" in c.lower() and "id" in c.lower()
]
cost_cols = [
    c for c in campaigns.columns
    if any(word in c.lower() for word in ["cost", "spend", "budget"])
]

if not campaign_cols or not cost_cols:
    print("\nCheck module12_campaign_data.csv for campaign ID and cost fields.")
    print("ROI calculation needs campaign-attributed revenue and campaign cost.")
else:
    print("Campaign ID column:", campaign_cols[0])
    print("Campaign cost column:", cost_cols[0])
    print("Match campaign-attributed transactions to calculate ROI.")

print("\nModule 12 campaign data preparation completed!")
print(f"Reports saved in: {out}")

