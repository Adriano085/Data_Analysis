import pandas as pd
import locale
from datetime import datetime
import os

locale.setlocale(locale.LC_ALL, "pt_BR.UTF-8")

root_path = os.path.dirname(os.path.abspath(__file__))

# Function to convert date strings to datetime format
def date_convert(date_text):
    try:
        # Convert "Wednesday, 22 of November 2023" to "22/11/2023"
        date = datetime.strptime(date_text, "%A, %d de %B de %Y")
        return pd.to_datetime(date, format="%d/%m/%Y")
    except ValueError:
        return None

df = pd.read_excel(f"{root_path}/data/dataset.xlsx")

# Convert date columns to datetime format
df["Data_Pedido"] = df["Data_Pedido"].apply(date_convert)
df["Data_Entrega_Prevista"] = df["Data_Entrega_Prevista"].apply(date_convert)
df["Data_Entrega_Realizada"] = df["Data_Entrega_Realizada"].apply(date_convert)

# Configurando a página


# Extract year and month from "Actual_Delivery_Date" for filtering
df['Ano_Entrega'] = df['Data_Entrega_Realizada'].dt.year
df['Mes_Entrega'] = df['Data_Entrega_Realizada'].dt.month


csv_file_path = f"{root_path}/data/processed_dataset.csv"

if os.path.exists(csv_file_path):
    os.remove(csv_file_path)

df.to_csv(csv_file_path, index=False)

