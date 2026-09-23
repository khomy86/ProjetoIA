"""Dataset de itinerários dos EUA (Expedia, 2022), já filtrado por filter_itineraries."""

import pandas as pd

TARGET = "totalFare"
CATEGORICAL_FEATURES = ["startingAirport", "destinationAirport", "segmentsAirlineName"]
DATE_FEATURES = ["dias_ate_voo", "mes_voo", "dia_semana_voo", "mes_pesquisa", "dia_semana_pesquisa"]


def load_itineraries(path):
    return pd.read_csv(
        path,
        parse_dates=["searchDate", "flightDate"],
        dtype=dict.fromkeys(CATEGORICAL_FEATURES, "category"),
    )


def add_date_features(df):
    return df.assign(
        dias_ate_voo=(df["flightDate"] - df["searchDate"]).dt.days.astype("int16"),
        mes_voo=df["flightDate"].dt.month.astype("int8"),
        dia_semana_voo=df["flightDate"].dt.dayofweek.astype("int8"),
        mes_pesquisa=df["searchDate"].dt.month.astype("int8"),
        dia_semana_pesquisa=df["searchDate"].dt.dayofweek.astype("int8"),
    )
