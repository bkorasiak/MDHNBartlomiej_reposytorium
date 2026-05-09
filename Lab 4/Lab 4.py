import pandas as pd
import numpy as np

# --- ZADANIE 1: Budowa pipeline ETL ---
# Krok 1: Extract (Wczytanie danych)
# Używamy kodowania ISO-8859-1, aby uniknąć błędów Unicode z poprzednich zajęć.
df = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# Krok 2: Transform (Czyszczenie i przygotowanie)
# 1. Usuwamy rekordy bez CustomerID
df = df.dropna(subset=["CustomerID"])
# 2. Usuwamy ujemne ilości i ceny (filtrowanie błędów)
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] >= 0)]
# 3. Usuwamy duplikaty
df = df.drop_duplicates()
# 4. Poprawa typów danych i rozbicie daty
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month
df["Day"] = df["InvoiceDate"].dt.day
# 5. Dodatkowa kolumna miary (Przychód) - ułatwia późniejszą analizę wartości sprzedaży
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Krok 3: Load (Zapis tabeli faktów z Zadania 1)
fact_sales = df[["InvoiceNo", "StockCode", "CustomerID", "InvoiceDate", "Quantity", "Revenue"]]
fact_sales.to_csv("fact_sales.csv", index=False)
print("Zadanie 1 zakończone: Utworzono fact_sales.csv")

# --- ZADANIE 2: Integracja danych z wielu źródeł ---
# Krok 1: Extract (Drugi dataset)
# Uwaga: Plik Online_Retail_II.xlsx musi być wgrany na PythonAnywhere
try:
    df2 = pd.read_excel("online_retail_II.xlsx")
    
    # Krok 2: Transform (Integracja i ujednolicenie)
    # Sprawdzamy czy nazwy kolumn są spójne. Jeśli nie, ujednolicamy do schematu z df1.
    # Wstępne czyszczenie df2 analogicznie do df1
    df2 = df2.dropna(subset=["Customer ID"]) # W II części nazwa może mieć spację
    df2.columns = df.columns[:8] # Próba ujednolicenia nazw kolumn do pierwszego zbioru
    
    # Krok 3: Merge (Połączenie zbiorów)
    # Używamy concat, ponieważ chcemy dokleić nowe rekordy pod spód
    df_all = pd.concat([df, df2], ignore_index=True)
    
    # Krok 4: Load (Zapis zintegrowanej tabeli faktów)
    df_all.to_csv("fact_sales_integrated.csv", index=False)
    print("Zadanie 2 zakończone: Utworzono fact_sales_integrated.csv")
except FileNotFoundError:
    print("Błąd: Brak pliku online_retail_II.xlsx. Wgraj go, aby wykonać Zadanie 2.")