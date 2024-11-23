import streamlit as st # Constução da dashboard
import pandas as pd
import plotly.express as px  # Usada para criar os graficos

# Com uma visão mensal
# faturamento por unidade…
# tipo de produto mais vendido, contribuição por filial,
# Desempenho das forma de pagamento…
# Como estão as avaliações das filiais?

st.set_page_config(layout="wide")

df = pd.read_csv("data/supermarket_sales.csv", sep=";", decimal=",")

df['Date'] = pd.to_datetime(df['Date']) # convert object to datetime
df['Date'] = df['Date'].dt.date #  Take off the timestamp
df= df.sort_values(by="Date") # sort by date

df

df['Month'] = df['Date'].apply(lambda x: str(x.year) + '-' + str(x.month))
month = st.sidebar.selectbox('Month', pd.unique(df['Month']))

df_filtered = df[df['Month'] == month]
# df_filtered

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

fig_date = px.bar(df_filtered, x="Date", y="Total", color="City", title="Faturamento por Dia")
col1.plotly_chart(fig_date, use_container_width=True)

prod_date = px.bar(df_filtered, x="Date", y="Product line", 
                  color="City", 
                  title="Faturamento por Produto",
                  orientation="h")
col2.plotly_chart(prod_date, use_container_width=True)

city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por Filia")
col3.plotly_chart(fig_city, use_container_width=True)

fig_pay = px.pie(df_filtered, values="Total", names="Payment", title="Faturamento por Produto")
col4.plotly_chart(fig_pay, use_container_width=True)

city_mean = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_review = px.bar(city_mean, x="City", y="Rating", title="Avaliações das Filiais")
col5.plotly_chart(fig_review, use_container_width=True)