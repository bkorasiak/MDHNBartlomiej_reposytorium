import pandas as pd

# 1. Wczytanie danych
df = pd.read_csv('sales_raw.csv')

# 2. Utworzenie kolumny z łączną wartością transakcji
df['total_value'] = df['quantity'] * df['unit_price']

# 3. Agregacje (Łączna sprzedaż)
# Sprzedaż wg kraju
sales_by_country = df.groupby('country')['total_value'].sum()

# Sprzedaż wg produktu
sales_by_product = df.groupby('product_name')['total_value'].sum()

# 4. Wybór transakcji powyżej 1000 i zapis do pliku
df_high_value = df[df['total_value'] > 1000]
df_high_value.to_csv('high_value_sales.csv', index=False)

# 5. Podsumowanie liczby transakcji w każdym kraju (dla zbioru powyżej 1000)
count_by_country = df_high_value.groupby('country').size()

print("Przetwarzanie zakończone. Plik 'high_value_sales.csv' został utworzony.")