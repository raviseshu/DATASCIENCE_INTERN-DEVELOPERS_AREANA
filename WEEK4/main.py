import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Load CSV file
df = pd.read_csv('data/sales_data.csv')

# Verify load
print(f"Loaded {len(df)} records")
print(df.head())


# Check for missing values
missing = df.isnull().sum()

# Fill missing
df['Quantity'].fillna(df['Quantity'].median(), inplace=True)
df['Unit_Price'].fillna(df['Unit_Price'].mean(), inplace=True)

# Verify cleaning
print("Data cleaned successfully")


# Calculate statistics
total_sales = df['Total_Sales'].sum()
avg_order = df['Total_Sales'].mean()
best_product = df.groupby('Product')['Total_Sales'].sum().idxmax()

print(f"Total Sales: ${total_sales:.2f}")
print(f"Average Order: ${avg_order:.2f}")
print(f"Best Product: {best_product}")


# Create subplots
fig, axes = plt.subplots(2, 2, figsize=(12, 8))

# Chart 1: Bar chart (sales by product)
product_sales = df.groupby('Product')['Total_Sales'].sum()
axes[0, 0].bar(product_sales.index, product_sales.values)
axes[0, 0].set_title('Sales by Product')

# Chart 2: Line chart (daily sales trend)
daily_sales = df.groupby('Date')['Total_Sales'].sum()
axes[0, 1].plot(daily_sales.index, daily_sales.values)
axes[0, 1].set_title('Daily Sales Trend')

# Chart 3: Pie chart (market share)
axes[1, 0].pie(product_sales.values, labels=product_sales.index, autopct='%1.1f%%')
axes[1, 0].set_title('Market Share by Product')

# Chart 4: Text summary
axes[1, 1].axis('off')
summary_text = f"""
Sales Summary
─────────────
Total Sales: ${total_sales:.2f}
Average Order: ${avg_order:.2f}
Top Product: {best_product}
Products: {df['Product'].nunique()}
"""
axes[1, 1].text(0.1, 0.5, summary_text, fontsize=12)

plt.tight_layout()
plt.savefig('visualizations/analysis_report.png', dpi=300)
plt.show()


# Create text report
report = f"""
═════════════════════════════════════════
        DATA ANALYSIS REPORT
═════════════════════════════════════════

PROJECT: Sales Data Analysis
DATE: {pd.Timestamp.now().strftime('%Y-%m-%d')}

KEY METRICS:
─────────────
Total Sales:        ${total_sales:,.2f}
Average Order:      ${avg_order:,.2f}
Total Transactions: {len(df)}
Products:           {df['Product'].nunique()}

TOP PRODUCTS:
─────────────
{product_sales.nlargest(3).to_string()}

INSIGHTS:
─────────
• {best_product} is our best-selling product
• Monthly trend shows {('increasing' if daily_sales.iloc[-1] > daily_sales.iloc else 'decreasing')} sales
• Customer base spans {df['Customer_ID'].nunique()} unique customers

RECOMMENDATIONS:
────────────────
✓ Focus marketing on {best_product}
✓ Investigate low-performing products
✓ Maintain customer relationships
"""

# Save report
with open('report/analysis_report.txt', 'w') as f:
    f.write(report)

print(report)

---

## <a name="visualization"></a>📊 DATA VISUALIZATION GUIDE

### **Creating Professional Charts**

#### **Chart 1: Bar Chart (Sales by Product)**


def create_bar_chart(df, output_path):
    """Create bar chart showing sales by product"""

    # Calculate sales by product
    product_sales = df.groupby('Product')['Total_Sales'].sum().sort_values(ascending=False)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bar chart
    bars = ax.bar(range(len(product_sales)), product_sales.values, color='steelblue')

    # Customize
    ax.set_title('Sales by Product', fontsize=16, fontweight='bold')
    ax.set_xlabel('Product', fontsize=12)
    ax.set_ylabel('Sales ($)', fontsize=12)
    ax.set_xticks(range(len(product_sales)))
    ax.set_xticklabels(product_sales.index, rotation=45, ha='right')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height,
                f'${height:,.0f}',
                ha='center', va='bottom', fontsize=10)

    # Add grid
    ax.grid(axis='y', alpha=0.3)

    # Layout and save
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✅ Bar chart saved: {output_path}")

    return fig
