import pandas as pd

df = pd.read_csv("sales_raw.csv")
df["total_value"] = df["quantity"] * df["unit_price"]

sales_by_country = df.groupby("country")["total_value"].sum()
sales_by_product = df.groupby("product_name")["total_value"].sum()

df_high_value = df[df["total_value"] > 1000]
df_high_value.to_csv("high_value_sales.csv", index=False)

transactions_by_country = df_high_value.groupby("country").size()