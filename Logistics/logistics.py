import pandas as pd
import plotly.express as px
import streamlit as st
import os
import calendar

root_path = os.path.dirname(os.path.abspath(__file__))
csv_file_path = f"{root_path}/data/processed_dataset.csv"
df = pd.read_csv(csv_file_path)

st.set_page_config(page_title="Logistics", page_icon="📦", layout="wide")

# Get unique years and months for dropdown options
available_years = df["Ano_Entrega"].unique()
available_months = ["Todos"] + [calendar.month_name[i] for i in sorted(df["Mes_Entrega"].unique())]

st.sidebar.header("Filters")
selected_year = st.sidebar.selectbox(
    "Select Year", options=sorted(available_years, reverse=True), index=0
)
selected_month = st.sidebar.selectbox("Select Month", options=available_months, index=0)

# Apply filters based on the selected month
if selected_month == "Todos":
    df_filtered = df[df["Ano_Entrega"] == selected_year]
else:
    month_number = list(calendar.month_name).index(selected_month)
    df_filtered = df[
        (df["Ano_Entrega"] == selected_year) & (df["Mes_Entrega"] == month_number)
    ]

on_time_deliveries = (
    df_filtered[df_filtered["Status_Entrega"] == "No Prazo"]
    .groupby("Canal_Entrega")["Status_Entrega"]
    .count()
    .reset_index(name="Total")
    .sort_values(by="Total",ascending=False)
)

fig = px.bar(
    on_time_deliveries,
    x="Canal_Entrega",
    y="Total",
    title=f"Deliveries in {selected_month}/{selected_year}",
)

# Display the line chart in the Streamlit app
st.plotly_chart(fig, use_container_width=True)
