# Assignment 2: Building a Clean Data Warehouse for Market Basket Discovery

## Overview

This project transitions a "dirty" retail sales dataset into a professionally modeled Star Schema data warehouse (SQLite), then performs Market Basket Analysis using the Apriori algorithm to discover product purchase patterns.

## Project Structure

```
Assignment 2 - Data Warehousing/
├── data/                          # Raw and cleaned datasets
│   ├── retail_store_sales.csv     # Original Kaggle dataset
│   └── cleaned_sales.csv         # Cleaned output (11,362 rows)
├── notebooks/                     # Jupyter notebooks (main code)
│   ├── 01_data_cleaning.ipynb    # Part A: Data Cleaning
│   ├── 02_star_schema.ipynb      # Part B: Star Schema Warehouse
│   └── 03_market_basket_analysis.ipynb  # Part C: Association Mining
├── warehouse/                     # SQLite database
│   └── sales_warehouse.db        # Star Schema warehouse
├── diagram/                       # Architecture diagrams
│   └── star_schema.png           # ER diagram of the Star Schema
├── screenshots/                   # Table screenshots
│   ├── DimDate.png
│   ├── DimProduct.png
│   ├── DimCustomer.png
│   ├── FactSales.png
│   └── JoinedWarehouseView.png
├── report/                        # Mining report and deliverables
│   ├── mining_report.md          # Written report
│   ├── visualizations/           # Charts and plots
│   │   ├── top10_category_associations.png
│   │   ├── top10_product_associations.png
│   │   ├── support_vs_confidence.png
│   │   └── monthly_lift_heatmap.png
│   └── data/                     # Supporting CSV data
│       ├── top5_associations.csv
│       ├── category_associations.csv
│       └── monthly_consistency.csv
└── requirements.txt              # Python dependencies
```

## Setup

```bash
pip install -r requirements.txt
```

## Running

Execute the notebooks in order:
1. `notebooks/01_data_cleaning.ipynb` -- Cleans and exports data
2. `notebooks/02_star_schema.ipynb` -- Builds the SQLite warehouse
3. `notebooks/03_market_basket_analysis.ipynb` -- Runs association mining
