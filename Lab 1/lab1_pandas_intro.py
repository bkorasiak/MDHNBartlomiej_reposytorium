import matplotlib
matplotlib.use("Agg")  # Ustawienie dla serwerów bez ekranu
import pandas as pd

# Krok 2: Wczytanie danych
df = pd.read_csv("sales_raw.csv")
print("--- Pierwsze 5 rekordów ---")
print(df.head())
print(f"Rozmiar tabeli: {df.shape}")

# Krok 3: Transformacje danych
df["order_date"] = pd.to_datetime(df["order_date"]) # Konwersja daty
df["total_value"] = df["quantity"] * df["unit_price"] # Miara sprzedaży
df["year"] = df["order_date"].dt.year # Atrybut czasu

# Krok 4: Agregacje (proste analizy)
total_sales = df["total_value"].sum()
sales_by_country = df.groupby("country")["total_value"].sum()
sales_by_year = df.groupby("year")["total_value"].sum()

print(f"\nCałkowita sprzedaż: {total_sales}")
print("\nSprzedaż wg krajów:")
print(sales_by_country)

# Krok 5: Zapisanie zagregowanych danych do nowego pliku
df_agg = df.groupby(["country", "year"])["total_value"].sum().reset_index()
df_agg.to_csv("sales_aggregated.csv", index=False)
print("\nPlik 'sales_aggregated.csv' został utworzony.")