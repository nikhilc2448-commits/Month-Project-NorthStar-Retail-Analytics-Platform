# Module 15 – Warehouse Design

## 1. Objective

Design and implement a retail data warehouse using a star schema to support sales analysis, business intelligence, and reporting.

## 2. Database

**Database Name:** `northstar_warehouse`

## 3. Schema Design

### Fact Table

**`fact_sales`** stores sales transaction records.

**Measures:**

* Quantity
* Unit Price
* Discount Amount
* Net Revenue
* Cost Amount
* Profit Margin

The fact table connects to dimension tables through foreign keys.

### Dimension Tables

* **`dim_date`:** Date, day, month, quarter, year, and weekend information.
* **`dim_customer`:** Customer details and RFM segment.
* **`dim_product`:** Product details, category, unit cost, and retail price.
* **`dim_store`:** Store details, region, and quarterly sales target.

## 4. Data Warehouse Grain

Each row in `fact_sales` represents one sales transaction record for a product on a particular date.

## 5. Loaded Data

| Table          | Total Rows |
| -------------- | ---------: |
| `dim_date`     |        630 |
| `dim_customer` |      3,000 |
| `dim_product`  |        520 |
| `dim_store`    |         18 |
| `fact_sales`   |     43,515 |

*Note: These are the latest verified table counts available from the project. The dimension counts should be rechecked if the warehouse is rebuilt.*

## 6. Sales Summary

| KPI                    |             Value |
| ---------------------- | ----------------: |
| Sales Records          |            43,515 |
| Unique Transactions    |            43,515 |
| Total Revenue          |   ₹918,207,848.73 |
| Total Quantity         |            59,352 |
| First Transaction Date |    1 January 2023 |
| Last Transaction Date  | 22 September 2024 |

**Note:** The source dataset contains 47,314 records, including 3,799 records with blank or invalid dates. These records have not been included in the date-based warehouse load. Source and warehouse revenue reconciliation remains in progress.

## 7. Relationships

The `fact_sales` table connects to the following dimension tables:

* `fact_sales.date_key` → `dim_date.date_key`
* `fact_sales.customer_key` → `dim_customer.customer_key`
* `fact_sales.product_key` → `dim_product.product_key`
* `fact_sales.store_key` → `dim_store.store_key`

These relationships support analysis by date, customer, product, and store.

## 8. Data Quality and Validation

The warehouse contains 43,515 records with valid transaction dates.

The following items require validation:

* Investigate 3,799 source records with blank or invalid dates.
* Reconcile source revenue of ₹1,001,820,681.02 against warehouse revenue of ₹918,207,848.73.
* Verify customer and store dimension mappings.
* Confirm that cost and profit fields contain valid business calculations before using them for profitability analysis.

The aggregate source-to-warehouse revenue difference is ₹83,612,832.29. This is an unreconciled reporting difference, not confirmed lost revenue.

## 9. Conclusion

The `northstar_warehouse` database has been populated with a star-schema structure consisting of one sales fact table and four dimension tables.

The current warehouse contains 43,515 unique transactions, recorded revenue of ₹918,207,848.73, and 59,352 units sold for the period from 1 January 2023 to 22 September 2024.

Further validation of source data quality, revenue reconciliation, dimension relationships, and profitability measures is required before the warehouse can be considered fully validated for executive reporting.
