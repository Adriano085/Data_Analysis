import pandas as pd
import plotly.express as px
import streamlit as st

from calculate import (
    calculate_on_time_delivery,
    calculate_total_deliveries,
    calculate_deliveries_by_month,
    calculate_percenge_status,
    calculate_percentage_team,
    city_delivery_summary,
    calculate_total_on_time,
    calculate_total_delay
)
from utils import (
    card_style,
    get_available_year,
    get_available_months,
    generate_df_filtered,
    df_filteredby_year,
)

# ---------------------------------------------PAGE CONFIG--------------------------------------------------#
st.set_page_config(page_title="Logistics", page_icon="📦", layout="wide")
# ----------------------------------------------------------------------------------------------------------#

# ----------------------------------------------SIDEBAR-----------------------------------------------------#
st.sidebar.header("Filtros")
years = get_available_year()
selected_year = st.sidebar.selectbox(
    "Selecione o Ano", options=sorted(years, reverse=True), index=0
)

months = get_available_months(selected_year)
selected_month = st.sidebar.selectbox("Selecione o Mês", options=months, index=0)
# ----------------------------------------------------------------------------------------------------------#

# --------------------------------------DF FILTERED---------------------------------------------------------#
# Apply filters based on the selected month
df_filtered = generate_df_filtered(selected_year, selected_month)
# ----------------------------------------------------------------------------------------------------------#

# -------------------------------------------MATRICS--------------------------------------------------------#
# Adding cards for metrics
st.sidebar.subheader("Métrica")
total_deliveries = calculate_total_deliveries(df_filtered)
total_on_time = calculate_total_on_time(df_filtered)
total_delay = calculate_total_delay(df_filtered)

st.sidebar.markdown(card_style.format(title="Total de Entregas", value=total_deliveries), unsafe_allow_html=True)
st.sidebar.markdown(card_style.format(title="Total de Entregas No Prazo", value=total_on_time), unsafe_allow_html=True)
st.sidebar.markdown(card_style.format(title="Total de Entregas Atrasadas", value=total_delay), unsafe_allow_html=True)
# ----------------------------------------------------------------------------------------------------------#

# ---------------------------------------MAIN DASHBOARD-----------------------------------------------------#
# Main dashboard layout
with st.container():

    st.header("📊 Dashboard de Entregas")

    # Columns configuration
    col1, col2 = st.columns(2)
    col3, col4, col5 = st.columns(3)

     # ----------------------------------------------CHART 01-----------------------------------------------#
    # On Time Delivery Chart
    on_time_deliveries = calculate_on_time_delivery(df_filtered)
    fig_channel = px.bar(
        on_time_deliveries,
        x="Canal_Entrega",
        y="Total",
        color="Status_Entrega",
        title=f"Total de Entregas por Canal",
        barmode="group"
    )
    # Display the line chart in the Streamlit app
    col1.plotly_chart(fig_channel, use_container_width=True)
    # ------------------------------------------------------------------------------------------------------#

    # ----------------------------------------------CHART 02------------------------------------------------#
    # Total Deliveries of Team by Month Chart
    df_team = calculate_percentage_team(df_filtered)
    df_team["FormattedPercentage"] = df_team["Percentage"].apply(lambda x: f"{x}%")
    fig_team = px.bar(
        df_team,
        y="Equipe_Entrega",
        x="Percentage",
        title="Percentual de Entregas Por Equipe",
        text="FormattedPercentage",

    )
    fig_team.update_traces(textposition="outside")
    col2.plotly_chart(fig_team, use_container_width=True)
    # -------------------------------------------------------------------------------------------------------#

    # -----------------------------------------------CHART 03------------------------------------------------#
    #  Deliveries by Month
    df_filtered_year = df_filteredby_year(selected_year)
    deliveries_by_month = calculate_deliveries_by_month(df_filtered_year)
    fig_month = px.line(
        deliveries_by_month,
        x="Mes_Entrega",
        y="Data_Entrega_Realizada",
        title="Total de Entregas Por Mês",
    )
    col3.plotly_chart(fig_month, use_container_width=True)
    # -------------------------------------------------------------------------------------------------------#

     # ----------------------------------------------CHART 04------------------------------------------------#
     # Percentage of Status
    df_status = calculate_percenge_status(df_filtered)
    fig_status = px.pie(
        df_status, names="Status_Entrega", values="Percentage", title="Percentual de Entregas Por Status"
    )
    col4.plotly_chart(fig_status, use_container_width=True)
    # -------------------------------------------------------------------------------------------------------#

    # -----------------------------------------------TABLE 01------------------------------------------------#
    # Summary of City Delivery
    df_city_summary = city_delivery_summary(df_filtered)
    col5.markdown(
    "<h5 style='font-size:16px;'>Resumo de Entregas por Cidade</h5>",
    unsafe_allow_html=True
)
    col5.dataframe(df_city_summary, use_container_width=True)