import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing

root = Path(__file__).resolve().parents[2]
data = root / "data" / "processed"
out = root / "reports" / "week2"
out.mkdir(parents=True, exist_ok=True)

# Load integrated sales data
df = pd.read_csv(data / "module4_analysis_ready.csv")
df["OrderDate"] = pd.to_datetime(df["OrderDate"], errors="coerce")
df["LineAmount"] = pd.to_numeric(df["LineAmount"], errors="coerce")
df = df.dropna(subset=["OrderDate", "LineAmount"])

# Aggregate sales monthly
monthly = (
    df.set_index("OrderDate")["LineAmount"]
    .resample("MS")
    .sum()
    .asfreq("MS", fill_value=0)
)

monthly.to_csv(out / "module9_monthly_sales.csv", header=["Sales"])

# Decompose trend and seasonality
decomposition = seasonal_decompose(
    monthly, model="additive", period=12, extrapolate_trend="freq"
)

decomposition_df = pd.DataFrame({
    "Sales": monthly,
    "Trend": decomposition.trend,
    "Seasonality": decomposition.seasonal,
    "Residual": decomposition.resid
})
decomposition_df.to_csv(out / "module9_sales_decomposition.csv")

# Plot decomposition
decomposition.plot()
plt.tight_layout()
plt.savefig(out / "module9_sales_decomposition.png", dpi=150)
plt.close()

# Forecast next quarter (3 months)
model = ExponentialSmoothing(
    monthly,
    trend="add",
    seasonal="add",
    seasonal_periods=12,
    initialization_method="estimated"
).fit()

forecast = model.forecast(3)
forecast_df = forecast.rename("ForecastSales").to_frame()
forecast_df.index.name = "Month"
forecast_df.to_csv(out / "module9_next_quarter_forecast.csv")

# Basic confidence assessment
mape = (abs((monthly - model.fittedvalues) / monthly.replace(0, float("nan")))).mean() * 100

if pd.notna(mape) and mape < 10:
    confidence = "Higher"
elif pd.notna(mape) and mape < 20:
    confidence = "Moderate"
else:
    confidence = "Low"

with open(out / "module9_forecast_summary.txt", "w", encoding="utf-8") as f:
    f.write(f"Forecast months: {', '.join(forecast.index.strftime('%b %Y'))}\n")
    f.write(f"Forecast sales:\n{forecast.to_string()}\n")
    f.write(f"Training MAPE: {mape:.2f}%\n" if pd.notna(mape) else "Training MAPE unavailable.\n")
    f.write(f"Initial confidence assessment: {confidence}\n")
    f.write("Note: This confidence assessment is based on training error, not a formal prediction interval.\n")

print("Module 9 completed successfully!")
print("\nNext-quarter sales forecast:")
print(forecast_df)
print(f"\nTraining MAPE: {mape:.2f}%" if pd.notna(mape) else "\nTraining MAPE unavailable.")
print(f"Initial confidence assessment: {confidence}")
print(f"\nReports saved to: {out}")