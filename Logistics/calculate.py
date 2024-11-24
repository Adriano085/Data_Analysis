import calendar


def calculate_on_time_delivery(df_date):
    data = (
        df_date.groupby(["Canal_Entrega", "Status_Entrega"])["Status_Entrega"]
        .count()
        .reset_index(name="Total")
        .sort_values(by=["Total"], ascending=False)
    )
    return data


def calculate_total_deliveries(df):
    total_deliveries = len(df)
    return total_deliveries


def calculate_total_on_time(df):
    on_time_deliveries_total = len(
        df[
            (df["Status_Entrega"] == "No Prazo")
            | (df["Status_Entrega"] == "Antecipado")
        ]["Status_Entrega"]
    )
    return on_time_deliveries_total

def calculate_total_delay(df):
    on_time_deliveries_total = len(
        df[
            (df["Status_Entrega"] == "Atrasado")
        ]["Status_Entrega"]
    )
    return on_time_deliveries_total

def calculate_deliveries_by_month(df):
    df_new = df.groupby("Mes_Entrega")["Data_Entrega_Realizada"].count().reset_index()
    df_new["Mes_Entrega"] = df_new["Mes_Entrega"].apply(
        lambda x: calendar.month_name[x]
    )
    return df_new


def calculate_percenge_status(df):
    df_status = (
        df.groupby(["Status_Entrega"])["Status_Entrega"]
        .count()
        .reset_index(name="Total")
    )

    percentage_status = (df_status["Total"] / df_status["Total"].sum()) * 100
    df_status["Percentage"] = round(percentage_status, 2)

    return df_status


def calculate_percentage_team(df):
    df_team_perc = (
        df.groupby("Equipe_Entrega")["Data_Entrega_Realizada"]
        .count()
        .reset_index(name="Total")
    )
    df_team_perc["Percentage"] = (
        df_team_perc["Total"] / df_team_perc["Total"].sum()
    ) * 100
    df_team_perc = round(
        df_team_perc.sort_values(by="Total", ascending=False), 2
    ).sort_values(by="Percentage", ascending=True)

    return df_team_perc


def city_delivery_summary(df):
    df_city = (
        df.groupby(["ID_Cidade", "Status_Entrega"])["Status_Entrega"]
        .count()
        .unstack(fill_value=0)  # Transform rows into columns, filling NaN with 0
    )
    df_city["Total"] = df_city[["No Prazo", "Atrasado", "Antecipado"]].sum(axis=1)
    df_city = df_city.sort_values(by="Total", ascending=False)
    df_city = df_city.rename(
        columns={
            "Antecipado": "Total_Antecipado",
            "No Prazo": "Total_No_Prazo",
            "Atrasado": "Total_Atrasado",
        }
    )
    return df_city
