import pandas as pd
import plotly.express as px
import streamlit as st

from calculate import (
    calculate_on_time_delivery,
    calculate_total_deliveries,
    calculate_total_on_time,
    calculate_deliveries_by_month,
    calculate_percenge_status,
    calculate_percentage_team,
    city_delivery_summary
)
from utils import (
    generate_plotly_card,
    get_available_year,
    get_available_months,
    generate_df_filtered,
    df_filteredby_year,
)


st.set_page_config(page_title="Logistics", page_icon="📦", layout="wide")

st.sidebar.header("Filters")

years = get_available_year()
selected_year = st.sidebar.selectbox(
    "Select Year", options=sorted(years, reverse=True), index=0
)

months = get_available_months(selected_year)
selected_month = st.sidebar.selectbox("Select Month", options=months, index=0)

col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)


# -----------------------------------------------------------------------------------------------------#
# Apply filters based on the selected month
df_filtered = generate_df_filtered(selected_year, selected_month)

# -----------------------------------------------------------------------------------------------------#
# Calculate the total number of deliveries and the total number of deliveries on-time.

# total_deliveries = calculate_total_deliveries(df_filtered)
# on_time_deliveries_total = calculate_total_on_time(df_filtered)

# # Generate and display the plotly cards with the calculated data.
# generate_plotly_card(total_deliveries, col1, "chart1")
# generate_plotly_card(on_time_deliveries_total, col2, "chart2")
# -----------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------#
on_time_deliveries = calculate_on_time_delivery(df_filtered)
fig_channel = px.bar(
    on_time_deliveries,
    x="Canal_Entrega",
    y="Total",
    color="Status_Entrega",
    title=f"Deliveries in {selected_month}/{selected_year}",
    barmode="group"
)
# Display the line chart in the Streamlit app
col1.plotly_chart(fig_channel, use_container_width=True)
# -----------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------#
df_team = calculate_percentage_team(df_filtered)
fig_team = px.bar(
    df_team,
    y="Equipe_Entrega",
    x="Percentage",
    title="Percentage of Deliveries by Team",
    text="Percentage",
)
fig_team.update_traces(textposition="outside")
fig_team.update_layout(width=900, height=400)
col2.plotly_chart(fig_team, use_container_width=True)
# -----------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------#
df_filtered_year = df_filteredby_year(selected_year)
deliveries_by_month = calculate_deliveries_by_month(df_filtered_year)
fig_month = px.line(
    deliveries_by_month,
    x="Mes_Entrega",
    y="Data_Entrega_Realizada",
    title="Deliveries by Month",
)
col3.plotly_chart(fig_month, use_container_width=True)
# -----------------------------------------------------------------------------------------------------#

# -----------------------------------------------------------------------------------------------------#
df_status = calculate_percenge_status(df_filtered)
fig_status = px.pie(
    df_status, names="Status_Entrega", values="Percentage", title="Status of Deliveries"
)
col4.plotly_chart(fig_status, use_container_width=True)
# -----------------------------------------------------------------------------------------------------#

city_delivery_summary = city_delivery_summary(df_filtered)
with col5:
    st.dataframe(city_delivery_summary)