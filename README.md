# NorthStar Retail Analytics Platform

## Project Overview

NorthStar Retail Analytics is a four-week end-to-end data analytics capstone project designed to build a unified analytics platform for a retail business operating across 18 stores in five states, along with online and mobile app channels.

The project integrates data from multiple internal systems, including POS transactions, customer records, product information, returns, inventory, marketing campaigns, and legacy store targets.

The objective is to transform raw business data into meaningful insights that support strategic and operational decision-making.

## Business Objectives

The platform addresses the following business questions:

1. Analyze overall business performance across stores, channels, regions, and product categories.
2. Identify valuable customer segments and purchasing behaviour.
3. Understand product returns and their financial impact.
4. Evaluate marketing campaign performance and ROI.
5. Identify inventory problems, stockouts, and slow-moving products.
6. Forecast sales for the next quarter.

## Dataset Description

The project uses eight source datasets:

| Dataset | Description |
|---|---|
| transactions.csv | Retail sales transactions |
| customers.csv | Customer information |
| products.csv | Product details |
| stores.csv | Store information |
| returns.csv | Product return records |
| inventory.csv | Inventory information |
| campaigns.json | Marketing campaign data |
| store_targets_legacy.csv | Legacy store sales targets |

## Project Modules

### Week 1 – Foundation

- Module 1: Data Ingestion (CSV and JSON)
- Module 2: Data Quality Audit
- Module 3: Data Cleaning and Standardization
- Module 4: Data Integration

### Week 2 – Data Analysis

- Module 5: NumPy and Pandas Analysis
- Module 6: Exploratory Data Analysis (EDA)
- Module 7: Statistical Analysis and Hypothesis Testing
- Module 8: Cohort and Customer Retention Analysis
- Module 9: Time Series Analysis and Sales Forecasting

### Week 3 – Advanced Analytics

- Module 10: Customer Segmentation using RFM and K-Means
- Module 11: Product Returns Analysis
- Module 12: Marketing ROI Analysis
- Module 13: Inventory Analysis
- Module 14: SQL Business Analysis

### Week 4 – Business Intelligence and Delivery

- Module 15: Data Warehouse Design (Star Schema)
- Module 16: Excel KPI Reporting
- Module 17: Power BI Dashboard
- Module 18: Executive Business Intelligence Report
- Module 19: GitHub Repository and Documentation

## Technologies Used

- Python
- Pandas
- NumPy
- SciPy
- Matplotlib
- Statsmodels
- MySQL
- Microsoft Excel
- Microsoft Power BI
- Git and GitHub
- JSON and CSV

## Project Folder Structure

```text
NorthStar-Retail-Analytics/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── module1/
│   ├── module2/
│   ├── module3/
│   ├── module4/
│   ├── module5/
│   ├── module6/
│   ├── module7/
│   ├── module8/
│   ├── module9/
│   ├── module10/
│   ├── module11/
│   ├── module12/
│   ├── module13/
│   ├── module14/
│   ├── module15/
│   ├── module16/
│   ├── module17/
│   └── module18/
│
├── logs/
├── notebooks/
├── reports/
│   ├── week1/
│   ├── week2/
│   ├── week3/
│   └── week4/
│
└── README.md
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

### 2. Navigate to the Project

```bash
cd NorthStar-Retail-Analytics
```

### 3. Install Required Libraries

```bash
pip install pandas numpy scipy matplotlib statsmodels openpyxl
```

### 4. Run Python Modules

Execute the Python scripts from the project root directory.

Example:

```bash
python src/module1/data_loader.py
python src/module2/data_quality_audit.py
python src/module3/clean_data.py
python src/module4/integrate_data.py
```

Continue with the remaining modules in sequence, ensuring the required input files and database tables are available.

## Key Deliverables

- Raw and cleaned datasets
- Data quality audit reports
- Data cleaning log
- Integrated analysis-ready dataset
- Statistical analysis and hypothesis testing reports
- Customer cohort and retention analysis
- Sales trend and forecasting reports
- Customer segmentation results
- Product returns analysis
- Marketing campaign analysis
- Inventory analysis
- SQL business queries
- Data warehouse schema
- Excel KPI workbook
- Power BI dashboard
- Executive business intelligence report

## Expected Business Value

The analytics platform is designed to help NorthStar Retail:

- Improve revenue visibility.
- Identify high-value customers.
- Reduce product return costs.
- Improve marketing investment decisions.
- Optimize inventory management.
- Support data-driven business planning.

## Conclusion

This project demonstrates an end-to-end data analytics workflow, covering data ingestion, data quality, cleaning, integration, statistical analysis, advanced analytics, SQL, data warehousing, Excel reporting, and Power BI visualization.

The final objective is to transform multiple disconnected business data sources into a unified analytics platform that supports informed business decisions.

---

**Project:** NorthStar Retail Analytics Platform  
**Project Duration:** Four Weeks  
**Domain:** Retail Analytics  
**Repository:** NorthStar-Retail-Analytics
