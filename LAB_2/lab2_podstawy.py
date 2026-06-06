import pandas as pd

df = pd.read_csv("sales_raw.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# Suma total_price i quantity dla każdego miesiąca i kraju
df["total_value"] = df["quantity"] * df["unit_price"]
df["month"] = df["order_date"].dt.to_period("M")
monthly_stats = df.groupby(["month", "country"])[["total_value", "quantity"]].sum()
monthly_stats.to_csv("monthly_analysis.csv")

# Średnia cena jednostkowa dla każdego produktu w kwartale
df["quarter"] = df["order_date"].dt.to_period("Q")
avg_price_quarter = df.groupby(["quarter", "product_name"])["unit_price"].mean()
avg_price_quarter.to_csv("avg_quarterly_price.csv")