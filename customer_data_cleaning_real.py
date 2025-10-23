
# Project 1 — Customer Data Cleaning + Insights
# Author: Maria Nova
# Dataset: Online Retail II (UCI)


import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_excel("Online_Retail_II.xlsx", sheet_name="Year 2010-2011")

print("Original columns:")
print(df.columns)


df.columns = df.columns.str.strip().str.lower().str.replace(" ", "")
print("\nStandardized columns:")
print(df.columns)


if "price" in df.columns:
    df = df.rename(columns={"price": "unitprice"})


df = df.dropna(subset=["description", "unitprice"])
df = df[df["quantity"] > 0]
df = df[df["unitprice"] > 0]


df["totalprice"] = df["quantity"] * df["unitprice"]


total_sales = df["totalprice"].sum()
unique_customers = df["customerid"].nunique()
unique_countries = df["country"].nunique()

print("\n Cleaning completed successfully!")
print("Rows after cleaning:", len(df))
print(f"Total Sales (£): {total_sales:,.2f}")
print("Unique Customers:", unique_customers)
print("Countries:", unique_countries)


df.to_csv("Online_Retail_Cleaned.csv", index=False)
print("\n Cleaned file saved as: Online_Retail_Cleaned.csv")



country_sales = (
    df.groupby("country")["totalprice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\n Top 10 Countries by Total Sales (£):")
print(country_sales)

product_sales = (
    df.groupby("description")["totalprice"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print("\n Top 10 Products by Total Sales (£):")
print(product_sales)


df["invoicedate"] = pd.to_datetime(df["invoicedate"])
df["month"] = df["invoicedate"].dt.to_period("M")
monthly_sales = df.groupby("month")["totalprice"].sum()

plt.figure(figsize=(10,5))
monthly_sales.plot(kind="line", marker="o", color="steelblue")
plt.title("Monthly Sales Trend (£)", fontsize=14)
plt.xlabel("Month")
plt.ylabel("Total Sales (£)")
plt.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()

print("\n Chart displayed successfully!")
