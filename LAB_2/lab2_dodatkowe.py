import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("sales_raw.csv")
df["order_date"] = pd.to_datetime(df["order_date"])

# Wykres trendu sprzedaży laptopów
laptop_sales = df[df["product_name"] == "Laptop"]
trend = laptop_sales.groupby(["order_date", "country"])["quantity"].sum().unstack()
trend.plot(kind='line', title='Trend sprzedaży laptopów')
plt.savefig("laptop_trend.png")