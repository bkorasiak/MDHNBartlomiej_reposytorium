import pandas as pd

"""
ODPOWIEDZI NA PYTANIA KONTROLNE (LAB 2 - REFLEKSJA):
1. Dlaczego model 3NF nie jest wygodny do analiz OLAP?
   Ponieważ dane są mocno rozproszone. Aby uzyskać prosty raport sprzedażowy,
   system musi łączyć wiele tabel, co spowalnia zapytania przy dużych zbiorach.
2. Co wymagałoby wielu joinów?
   Analiza sprzedaży produktów według krajów i miesięcy wymagałaby połączenia
   wszystkich tabel: OrderItems -> Orders -> Customers -> Products -> Date.
"""

# --- ZADANIE 1: Wczytanie danych ---
url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"
df = pd.read_csv(url, encoding="ISO-8859-1")

print(f"Liczba rekordów: {len(df)}")
print(f"Liczba kolumn: {len(df.columns)}")
print("Przykładowe wiersze:")
print(df.head())

# --- ZADANIE 2 & 3: Identyfikacja encji i Model 3NF (Inmon) ---

# 1. Encja Customers (Klienci)
customers = df[['CustomerID', 'Country']].drop_duplicates()
# Usuwamy wiersze bez CustomerID, bo to klucz główny (PK)
customers = customers.dropna(subset=['CustomerID'])

# 2. Encja Products (Produkty)
products = df[['StockCode', 'Description']].drop_duplicates()

# 3. Encja Orders (Zamówienia)
orders = df[['InvoiceNo', 'InvoiceDate', 'CustomerID']].drop_duplicates()

# 4. Encja OrderItems (Pozycje zamówienia)
order_items = df[['InvoiceNo', 'StockCode', 'Quantity', 'UnitPrice']]

# 5. Encja Date (Opcjonalna - wymiar czasu)
dates = pd.DataFrame()
dates['InvoiceDate'] = df['InvoiceDate'].drop_duplicates()
dates['Year'] = pd.to_datetime(dates['InvoiceDate']).dt.year
dates['Month'] = pd.to_datetime(dates['InvoiceDate']).dt.month

# --- SPRAWDZENIE POPRAWNOŚCI KLUCZY ---
print("\nSprawdzanie kluczy głównych (czy są unikalne):")
print(f"Customers PK unikalny: {customers['CustomerID'].is_unique}")
print(f"Products PK unikalny: {products['StockCode'].is_unique}")
print(f"Orders PK unikalny: {orders['InvoiceNo'].is_unique}")

print("\nSprawdzanie kluczy obcych (czy relacje istnieją):")
print(f"OrderItems -> Products (FK): {order_items['StockCode'].isin(products['StockCode']).all()}")
print(f"OrderItems -> Orders (FK): {order_items['InvoiceNo'].isin(orders['InvoiceNo']).all()}")

# --- ZAPIS DO PLIKÓW ---
customers.to_csv("Inmon_Customers.csv", index=False)
products.to_csv("Inmon_Products.csv", index=False)
orders.to_csv("Inmon_Orders.csv", index=False)
order_items.to_csv("Inmon_OrderItems.csv", index=False)

print("\nModel 3NF został pomyślnie utworzony i zapisany.")