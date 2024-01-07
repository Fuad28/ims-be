from datetime import datetime
import joblib
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras


def create_date_features(df):
    df["month"] = df.date.dt.month
    df["day_of_month"] = df.date.dt.day
    df["day_of_year"] = df.date.dt.dayofyear
    df["week_of_year"] = df.date.dt.isocalendar().week.astype("int64")
    df["day_of_week"] = df.date.dt.dayofweek + 1
    df["year"] = df.date.dt.year
    df["is_wknd"] = df.date.dt.weekday // 4
    df["quarter"] = df.date.dt.quarter
    df["is_month_start"] = df.date.dt.is_month_start.astype(int)
    df["is_month_end"] = df.date.dt.is_month_end.astype(int)
    df["is_quarter_start"] = df.date.dt.is_quarter_start.astype(int)
    df["is_quarter_end"] = df.date.dt.is_quarter_end.astype(int)
    df["is_year_start"] = df.date.dt.is_year_start.astype(int)
    df["is_year_end"] = df.date.dt.is_year_end.astype(int)
    # 0: Winter - 1: Spring - 2: Summer - 3: Fall
    df["season"] = np.where(df.month.isin([12, 1, 2]), 0, 1)
    df["season"] = np.where(df.month.isin([6, 7, 8]), 2, df["season"])
    df["season"] = np.where(df.month.isin([9, 10, 11]), 3, df["season"])

    return df


def run_inference(
    product_id: int,
    last_demand: float,
    start_date: None | datetime = None,
    end_date: None | datetime = None,
) -> float:
    """Performs inference on the given data over the specified time."""

    keras.backend.clear_session()

    SCALER_PATH = "oil_prevDem.joblib"
    SCALERY_PATH = "sales scaler.joblib"
    MODEL_PATH = "final model.h5"
    MEAN_OIL_PRICE = 67.7

    scalerOPd = joblib.load(SCALER_PATH)
    scalerOut = joblib.load(SCALERY_PATH)
    model = keras.models.load_model(MODEL_PATH)

    if not end_date:
        end_date = datetime(datetime.now().year, 12, 31)

    if not start_date:
        start_date = datetime.now()

    current_date = start_date

    cols = [
        "family",
        "onpromotion",
        "dcoilwtico",
        "month",
        "day_of_month",
        "day_of_year",
        "week_of_year",
        "is_wknd",
        "is_month_start",
        "is_month_end",
        "is_quarter_start",
        "is_quarter_end",
        "is_year_start",
        "is_year_end",
        "previous_demand",
        "locale_Local",
        "locale_National",
        "locale_Regional",
        "locale_no holiday",
        "day_of_week_1",
        "day_of_week_2",
        "day_of_week_3",
        "day_of_week_4",
        "day_of_week_5",
        "day_of_week_6",
        "day_of_week_7",
        "quarter_1",
        "quarter_2",
        "quarter_3",
        "quarter_4",
        "season_0",
        "season_1",
        "season_2",
        "season_3",
    ]

    # data=
    data = pd.DataFrame(
        {
            "date": [start_date],
            "family": [product_id],
            "onpromotion": [0],
            "dcoilwtico": [MEAN_OIL_PRICE],
            "locale_Local": [0],
            "locale_National": [0],
            "locale_Regional": [0],
            "locale_no holiday": [1],
            "day_of_week_1": [0],
            "day_of_week_2": [0],
            "day_of_week_3": [0],
            "day_of_week_4": [0],
            "day_of_week_5": [0],
            "day_of_week_6": [0],
            "day_of_week_7": [0],
            "quarter_1": [0],
            "quarter_2": [0],
            "quarter_3": [0],
            "quarter_4": [0],
            "season_0": [0],
            "season_1": [0],
            "season_2": [0],
            "season_3": [0],
        }
    )

    data = create_date_features(data)
    data["previous_demand"] = last_demand

    # run model
    days = (end_date - start_date).days
    total_demand = 0

    for _ in range(days):
        day_of_week = data["day_of_week"].tolist()[0]

        if day_of_week == 1:
            data["day_of_week_1"] = 1

        if day_of_week == 2:
            data["day_of_week_2"] = 1

        if day_of_week == 3:
            data["day_of_week_3"] = 1

        if day_of_week == 4:
            data["day_of_week_4"] = 1

        if day_of_week == 5:
            data["day_of_week_5"] = 1

        if day_of_week == 6:
            data["day_of_week_6"] = 1

        season = data["season"].tolist()[0]
        quarter = data["quarter"].tolist()[0]

        data[season] = 1
        data[quarter] = 1

        data[["dcoilwtico", "previous_demand"]] = scalerOPd.transform(
            data[["dcoilwtico", "previous_demand"]]
        )
        current_date = current_date + datetime.timedelta(days=1)
        data["date"] = current_date

        X = data[cols].values
        demand = abs(scalerOut.inverse_transform(model.predict(X)))
        data["previous_demand"] = np.random.uniform(0, demand.tolist()[0])
        total_demand += demand

    return total_demand


def compute_eoq(
    demand: float, unit_cost: int, ordering_cost: float, holding_cost: float
) -> float:
    """Computes the Economic Order Quantity"""

    if not holding_cost:
        holding_cost = np.random.uniform(0.2, 0.3) * unit_cost

    if not ordering_cost:
        ordering_cost = np.random.uniform(2, 300)

    eoq = np.sqrt(2 * ordering_cost * demand / holding_cost)

    return eoq


# demand, product_id = run_inference(
#     product_id="AUTOMOTIVE",
#     last_demand=0, # previous day's demand
#     start_date=[2023, 1, 1],
#     end_date=[2023, 1, 31],
# )
# print(compute_eoq(demand, product_id, [1, 120]))

# data["onpromotion"] = np.random.uniform(0, 10)
# data["dcoilwtico"] = np.random.uniform(60, 75)
# data["previous_demand"] = np.random.uniform(0, demand.tolist()[0])

# match season:
#     case "season_0":
#         data["season_0"] = 1
#     case "season_1":
#         data["season_1"] = 1
#     case "season_2":
#         data["season_2"] = 1
#     case "season_3":
#         data["season_3"] = 1

# match quarter:
#     case "quarter_1":
#         data["quarter_1"] = 1
#     case "quarter_2":
#         data["quarter_2"] = 1
#     case "quarter_3":
#         data["quarter_3"] = 1
#     case "quarter_4":
#         data["quarter_4"] = 1
