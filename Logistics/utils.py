import plotly.graph_objects as go
import os
import pandas as pd
import calendar

root_path = os.path.dirname(os.path.abspath(__file__))
csv_file_path = f"{root_path}/data/processed_dataset.csv"
df = pd.read_csv(csv_file_path)

def generate_plotly_card(total, col, key):
    fig = go.Figure()
    fig.update_layout(
        height=100,  # Altura do card
        width=250,   # Largura do card
        margin=dict(l=5, r=5, t=5, b=5)  # Margens
    )
    fig.add_trace(
        go.Indicator(
            mode="number",
            value=total,
            title={"text": "Total Deliveries"},
        )
    )
    return col.plotly_chart(fig, use_container_width=True, key=key)

def get_available_year():
# Get unique years and months for dropdown options
  available_years = df["Ano_Entrega"].unique()
  return available_years


def get_available_months(year):
   df_filtered_by_year = df[(df["Ano_Entrega"] == year)]["Mes_Entrega"].unique()
   available_months = ["Todos"] + [calendar.month_name[i] for i in sorted(df_filtered_by_year)]
   return available_months
   

def generate_df_filtered(selected_year, selected_month):
  if selected_month == "Todos":
      df_filtered = df[df["Ano_Entrega"] == selected_year]
  else:
      month_number = list(calendar.month_name).index(selected_month)
      df_filtered = df[(df["Ano_Entrega"] == selected_year) & (df["Mes_Entrega"] == month_number)]
  return df_filtered

def df_filteredby_year(selected_year):
   return df[(df["Ano_Entrega"] == selected_year)]

card_style = """
    <div style="
        padding: 10px;
        border-radius: 10px;
        background-color: #f4f4f4;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        margin-bottom: 25px;
        color: #333;
        text-align: center; 
    ">
        <h4 style="margin: 0;">{title}</h4>
        <p style="font-size: 24px; font-weight: bold; margin: 0;">{value}</p>
    </div>
"""