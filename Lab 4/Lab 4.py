import pandas as pd
import numpy as np

"""
ODPOWIEDZI NA PYTANIA KONTROLNE (LAB 4):
1. Przychód i wartość sprzedaży: Dodaliśmy kolumnę 'Revenue' (Quantity * UnitPrice),
   aby uniknąć powtarzania obliczeń w raportach.
2. Dodatkowe kolumny: Rozbicie daty na Year, Month, Day optymalizuje filtrowanie
   i grupowanie danych czasowych w hurtowni.
3. Integracja: Wybraliśmy 'pd.concat', ponieważ oba zbiory mają tę samą strukturę
   i reprezentują kolejne okresy, co pozwala na stworzenie jednej tabeli faktów.
4. Jakość danych: Filtrowanie brakujących CustomerID i ujemnych wartości
   zapewnia spójność i wiarygodność miar w modelu.
"""

# --- ZADANIE 1: ETL Pipeline ---
print("Uruchamianie Zadania 1...")

# Extract: Wczytanie z kodowaniem ISO-8859-1 dla uniknięcia błędów Unicode
df1 = pd.read_csv("Online_Retail.csv", encoding="ISO-8859-1")

# Transform: Czyszczenie i przygotowanie miar
df1 = df1.dropna(subset=["CustomerID"])
df1 = df1[(df1["Quantity"] > 0) & (df1["UnitPrice"] >= 0)]
df1 = df1.drop_duplicates()

# Transform: Przygotowanie wymiaru czasu i miary Revenue
df1["InvoiceDate"] = pd.to_datetime(df1["InvoiceDate"])
df1["Year"] = df1["InvoiceDate"].dt.year
df1["Month"] = df1["InvoiceDate"].dt.month
df1["Day"] = df1["InvoiceDate"].dt.day
df1["Revenue"] = df1["Quantity"] * df1["UnitPrice"]

# Load: Zapis podstawowej tabeli faktów
df1.to_csv("fact_sales.csv", index=False)
print("Utworzono: fact_sales.csv")


# --- ZADANIE 2: Integracja wielu źródeł ---
print("\nUruchamianie Zadania 2...")

try:
    # Extract: Wczytanie drugiego źródła (XLSX)
    df2 = pd.read_excel("online_retail_II.xlsx")

    # Transform: Ujednolicenie nazw kolumn (rozwiązanie konfliktu nazw)
    # W zbiorze II kolumna klienta często nazywa się 'Customer ID' (ze spacją)
    df2.columns = [c.replace(" ", "") for c in df2.columns]

    # Czyszczenie zbioru II przed połączeniem
    df2 = df2.dropna(subset=["CustomerID"])
    df2 = df2[(df2["Quantity"] > 0) & (df2["Price"] >= 0)] # W II może być 'Price' zamiast 'UnitPrice'
    df2 = df2.rename(columns={"Price": "UnitPrice"})

    # Merge: Połączenie (concat) - zachowujemy wszystkie rekordy z obu lat
    df_all = pd.concat([df1, df2], ignore_index=True)

    # Load: Zapis zintegrowanej hurtowni
    df_all.to_csv("fact_sales_integrated.csv", index=False)
    print("Utworzono: fact_sales_integrated.csv")

except FileNotFoundError:
    print("Błąd: Plik online_retail_II.xlsx nie został znaleziony. Pomiń Zadanie 2 lub wgraj plik.")

print("\nProces ETL zakończony pomyślnie.")