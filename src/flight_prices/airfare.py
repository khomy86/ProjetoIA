"""Dataset "Airfare ML" (EaseMyTrip, Índia, 2022), com preços convertidos para euros."""

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

INR_TO_EUR = 0.0111

TARGET = "Fare"
NUMERIC_FEATURES = ["Duration_in_hours", "Days_left"]
CATEGORICAL_FEATURES = [
    "Journey_day",
    "Airline",
    "Class",
    "Source",
    "Departure",
    "Total_stops",
    "Arrival",
    "Destination",
]


def load_airfare(path):
    data = pd.read_csv(path).drop(columns=["Date_of_journey", "Flight_code"])
    data[TARGET] = data[TARGET] * INR_TO_EUR
    return data


def remove_outliers_iqr(df, columns, factor=1.5):
    for column in columns:
        q1, q3 = df[column].quantile([0.25, 0.75])
        iqr = q3 - q1
        df = df[df[column].between(q1 - factor * iqr, q3 + factor * iqr)]
    return df


def build_pipeline(model):
    preprocessor = ColumnTransformer(
        [
            ("num", StandardScaler(), NUMERIC_FEATURES),
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
        ]
    )
    return Pipeline([("preprocessor", preprocessor), ("model", model)])
