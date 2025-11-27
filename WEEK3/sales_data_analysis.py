# ================================================
# Week 3 Project: Sales Data Analysis
# ================================================
# Analyze sales data to extract business insights

import pandas as pd
import numpy as np

# Step 1: Load the data
print("="*50)
print("SALES DATA ANALYSIS PROJECT")
print("="*50)
print()

# Read CSV file
df = pd.read_csv('sales_data.csv')

print("Step 1: Data Loading Complete")
print(f"Loaded {len(df)} records")
print()

# Step 2: Explore the data
print("="*50)
print("DATA EXPLORATION")
print("="*50)
print()

print("First 5 rows of data:")
print(df.head())
print()

print("Dataset Information:")
print(df.info())
print()

print("Dataset Shape:", df.shape)
print()

# Step 3: Check for missing values
print("="*50)
print("DATA QUALITY CHECK")
print("="*50)
print()

missing_values = df.isnull().sum()
print("Missing Values per Column:")
print(missing_values)
print()

# Calculate percentage of missing data
missing_percent = (missing_values / len(df)) * 100
print("Percentage of Missing Data:")
print(missing_percent)
print()

# Step 4: Clean the data
print("="*50)
print("DATA CLEANING")
print("="*50)
print()

# Save original count
original_count = len(df)

# Fill missing Quantity with median
if df['Quantity'].isnull().sum() > 0:
    median_quantity = df['Quantity'].median()
    df['Quantity'].fillna(median_quantity, inplace=True)
    print(f"Filled {missing_values['Quantity']} missing Quantity values with median: {median_quantity}")

# Fill missing Unit_Price with mean
if df['Unit_Price'].isnull().sum() > 0:
    mean_price = df['Unit_Price'].mean()
    df['Unit_Price'].fillna(mean_price, inplace=True)
    print(f"Filled {missing_values['Unit_Price']} missing Unit_Price values with mean: ${mean_price:.2f}")

# Recalculate Total_Sales for filled values
df['Total_Sales'] = df['Quantity'] * df['Unit_Price']

print()
print(f"Data cleaned successfully!")
print(f"Records before cleaning: {original_count}")
print(f"Records after cleaning: {len(df)}")
print()

# Step 5: Statistical Analysis
print("="*50)
print("STATISTICAL ANALYSIS")
print("="*50)
print()

print("Overall Statistics:")
print(df.describe())
print()

# Total sales
total_revenue = df['Total_Sales'].sum()
print(f"Total Revenue: ${total_revenue:,.2f}")

# Average order value
avg_order = df['Total_Sales'].mean()
print(f"Average Order Value: ${avg_order:.2f}")

# Total quantity sold
total_quantity = df['Quantity'].sum()
print(f"Total Units Sold: {int(total_quantity)}")

# Number of unique customers
unique_customers = df['Customer_ID'].nunique()
print(f"Unique Customers: {unique_customers}")

# Number of unique products
unique_products = df['Product'].nunique()
print(f"Unique Products: {unique_products}")
print()

# Step 6: Product Analysis
print("="*50)
print("PRODUCT PERFORMANCE ANALYSIS")
print("="*50)
print()

# Sales by product
product_sales = df.groupby('Product').agg({
    'Quantity': 'sum',
    'Total_Sales': ['sum', 'mean', 'count']
}).round(2)

product_sales.columns = ['Total_Quantity', 'Total_Sales', 'Avg_Sale', 'Order_Count']
product_sales = product_sales.sort_values('Total_Sales', ascending=False)

print("Sales Performance by Product:")
print(product_sales)
print()

# Best-selling product
best_product = product_sales.index[0]
best_product_sales = product_sales.loc[best_product, 'Total_Sales']

print(f"🏆 BEST-SELLING PRODUCT: {best_product}")
print(f"   Total Sales: ${best_product_sales:,.2f}")
print(f"   Units Sold: {int(product_sales.loc[best_product, 'Total_Quantity'])}")
print(f"   Orders: {int(product_sales.loc[best_product, 'Order_Count'])}")
print()

# Worst-selling product
worst_product = product_sales.index[-1]
worst_product_sales = product_sales.loc[worst_product, 'Total_Sales']

print(f"⚠️  NEEDS ATTENTION: {worst_product}")
print(f"   Total Sales: ${worst_product_sales:,.2f}")
print(f"   Units Sold: {int(product_sales.loc[worst_product, 'Total_Quantity'])}")
print(f"   Orders: {int(product_sales.loc[worst_product, 'Order_Count'])}")
print()

# Step 7: Generate Business Report
print("="*50)
print("BUSINESS INSIGHTS REPORT")
print("="*50)
print()

print("KEY FINDINGS:")
print()

# Calculate market share
product_sales['Market_Share'] = (product_sales['Total_Sales'] / total_revenue * 100).round(2)

print("1. Revenue Distribution:")
for product in product_sales.index[:3]:
    share = product_sales.loc[product, 'Market_Share']
    sales = product_sales.loc[product, 'Total_Sales']
    print(f"   - {product}: ${sales:,.2f} ({share}%)")
print()

# Average order value by product
print("2. Average Order Value by Product:")
top_aov = product_sales.nlargest(3, 'Avg_Sale')
for product in top_aov.index:
    aov = top_aov.loc[product, 'Avg_Sale']
    print(f"   - {product}: ${aov:.2f}")
print()

# Most popular products (by order count)
print("3. Most Popular Products (by Order Count):")
top_popular = product_sales.nlargest(3, 'Order_Count')
for product in top_popular.index:
    orders = int(top_popular.loc[product, 'Order_Count'])
    print(f"   - {product}: {orders} orders")
print()

print("RECOMMENDATIONS:")
print()
print(f"✓ Focus marketing efforts on '{best_product}' - it's your star product")
print(f"✓ Investigate why '{worst_product}' is underperforming")
print(f"✓ Consider bundling low-sellers with popular products")
print(f"✓ Total revenue of ${total_revenue:,.2f} from {len(df)} transactions")
print()

print("="*50)
print("ANALYSIS COMPLETE!")
print("="*50)

# Step 8: Save cleaned data and report
df.to_csv('sales_data_cleaned.csv', index=False)
product_sales.to_csv('product_performance_report.csv')

print()
print("Files saved:")
print("- sales_data_cleaned.csv (cleaned dataset)")
print("- product_performance_report.csv (analysis results)")
