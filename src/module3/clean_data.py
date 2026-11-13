import pandas as pd
from pathlib import Path

root = Path(__file__).resolve().parents[2]
raw = root / "data" / "raw"
out = root / "data" / "processed"
log_file = root / "logs" / "module3_data_cleaning_log.csv"

out.mkdir(parents=True, exist_ok=True)
log_file.parent.mkdir(parents=True, exist_ok=True)

logs = []


def log(file, action, details):
    logs.append({
        "file": file,
        "action": action,
        "details": details
    })


def clean(file):
    df = pd.read_csv(raw / file)
    original_rows = len(df)

    # Remove duplicate rows
    duplicates = df.duplicated().sum()
    df = df.drop_duplicates()

    if duplicates:
        log(file, "Remove duplicates", f"{duplicates} duplicate rows removed")

    # Clean text columns
    for col in df.select_dtypes(include=["object", "str"]).columns:
        df[col] = df[col].str.strip()

    log(file, "Standardize text", "Removed leading/trailing spaces")

    # Fill missing values
    for col in df.columns:
        if df[col].isna().sum() == 0:
            continue

        if pd.api.types.is_numeric_dtype(df[col]):
            df[col] = df[col].fillna(df[col].median())
            action = "Filled numeric missing values with median"
        else:
            df[col] = df[col].fillna("Unknown")
            action = "Filled text missing values with Unknown"

        log(file, action, f"Column: {col}")

    # Convert date columns
    for col in df.columns:
        if "date" in col.lower() or "month" in col.lower():
            df[col] = pd.to_datetime(
                df[col], errors="coerce"
            )

    # Save cleaned file
    name = Path(file).stem
    df.to_csv(
        out / f"module3_{name}_clean.csv",
        index=False
    )

    log(
        file,
        "Completed",
        f"Rows: {original_rows} → {len(df)}"
    )


files = [
    "transactions.csv",
    "customers.csv",
    "products.csv",
    "stores.csv",
    "returns.csv",
    "inventory.csv",
    "store_targets_legacy.csv"
]

for file in files:
    clean(file)

pd.DataFrame(logs).to_csv(log_file, index=False)

print("✓ Module 3 cleaning completed")
print(f"✓ Cleaning log: {log_file}")