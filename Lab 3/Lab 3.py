import pandas as pd
import datetime

# --- KROK 1: PRZYGOTOWANIE DANYCH ---
# Wczytujemy zbiór Online Retail.csv[cite: 18].
# Celem jest przygotowanie danych do modelu gwiazdy poprzez usunięcie błędnych rekordów[cite: 130].
df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# Usunięcie rekordów bez CustomerID, transakcji anulowanych (C) oraz wartości <= 0[cite: 135, 136, 137, 138].
# Działanie to zapobiega zafałszowaniu wyników przez błędne dane (zasada Garbage In, Garbage Out)[cite: 153].
df = df.dropna(subset=["CustomerID"])
df = df[~df["InvoiceNo"].str.startswith("C", na=False)]
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df = df.drop_duplicates()
df["Revenue"] = df["Quantity"] * df["UnitPrice"] # Dodanie kolumny miary przychodu[cite: 141].

# --- KROK 2: WYBÓR ZIARNA (GRAIN) ---
# Wybrano ziarno na poziomie pojedynczej pozycji faktury (InvoiceNo + StockCode)[cite: 175].
# Uzasadnienie: Pozwala to na najbardziej szczegółową analizę sprzedaży poszczególnych produktów[cite: 93].
# Przykład analizy: Identyfikacja najczęściej kupowanych produktów przez konkretnych klientów[cite: 181].

# --- KROK 3: BUDOWA TABEL WYMIARÓW I KLUCZY SZTUCZNYCH ---
# Wprowadzamy klucze sztuczne (Surrogate Keys), aby uniezależnić hurtownię od zmian w systemach źródłowych[cite: 227].

# Wymiar Produktu
dim_product = df[["StockCode", "Description"]].drop_duplicates().reset_index(drop=True)
dim_product["ProductSK"] = dim_product.index + 1

# Wymiar Kraju (Zadanie 2 - Rozszerzenie modelu)[cite: 269].
dim_country = df[["Country"]].drop_duplicates().reset_index(drop=True)
dim_country["CountrySK"] = dim_country.index + 1

# Wymiar Klienta z implementacją SCD Typu 2 (Wersjonowanie)[cite: 236, 277].
# Uzasadnienie: SCD 2 pozwala na śledzenie historii klienta bez nadpisywania starych danych[cite: 239].
dim_customer = df[["CustomerID", "Country"]].drop_duplicates().reset_index(drop=True)
dim_customer = dim_customer.merge(dim_country, on="Country").drop(columns=["Country"])
dim_customer["CustomerSK"] = dim_customer.index + 1
dim_customer["StartDate"] = pd.to_datetime("2026-01-01") # Data rozpoczęcia obowiązywania rekordu[cite: 279].
dim_customer["EndDate"] = pd.to_datetime("2261-12-31")  # Data zakończenia obowiązywania rekordu[cite: 279].
dim_customer["IsCurrent"] = True                         # Flaga aktualnego rekordu[cite: 280].

# Wymiar Czasu
dim_date = pd.DataFrame({"InvoiceDate": df["InvoiceDate"].unique()})
dim_date["DateSK"] = dim_date.index + 1

# --- KROK 4: BUDOWA TABELI FAKTÓW ---
# Tabela FactSales używa wyłącznie kluczy sztucznych i zawiera miary Quantity oraz Revenue[cite: 214, 230].
fact_sales = df.merge(dim_product, on=["StockCode", "Description"], how="left") \
               .merge(dim_customer, on="CustomerID", how="left") \
               .merge(dim_date, on="InvoiceDate", how="left")

fact_sales = fact_sales[["ProductSK", "CustomerSK", "DateSK", "Quantity", "Revenue"]]

# --- KROK 5: EKSPORT I PODSUMOWANIE ---
# Wynikowe tabele tworzą poprawny schemat gwiazdy[cite: 254].
fact_sales.to_csv("FactSales.csv", index=False)
dim_product.to_csv("DimProduct.csv", index=False)
dim_customer.to_csv("DimCustomer.csv", index=False)
dim_country.to_csv("DimCountry.csv", index=False)
dim_date.to_csv("DimDate.csv", index=False)

print("Hurtownia danych została zaimplementowana pomyślnie.")
"""
ODPOWIEDZI NA PYTANIA KONTROLNE (LAB 3):
1. Ziarno (Grain): Ziarnem tabeli faktów jest pojedyncza pozycja na fakturze
   (identyfikowana przez InvoiceNo i StockCode).
2. Klucze sztuczne (Surrogate Keys): Zastosowano CustomerSK i ProductSK, aby
   uniezależnić hurtownię od zmian w systemach źródłowych i umożliwić wersjonowanie SCD2.
3. SCD Typu 2: Zaimplementowano kolumny StartDate, EndDate i IsCurrent dla wymiaru klienta,
   co pozwala na śledzenie historycznych zmian danych bez nadpisywania starych rekordów.
4. Data graniczna: Wybrano rok 2261 jako EndDate dla aktywnych rekordów ze względu
   na limity biblioteki Pandas (limit nanosekundowy).
"""