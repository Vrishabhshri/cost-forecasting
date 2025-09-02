import pandas as pd
import numpy as np 

def add_time_features(df: pd.DataFrame):
    df = df.copy()
    df["d"] = pd.to_datetime(df["d"])
    df = df.sort_values(["practice_id", "d"])

    for k in [1, 7, 28]:
        df[f"paid_lag{k}"] = df.groupby("practice_id")["paid"].shift(k)

    for w in [7, 28, 84]:
        df[f"paid_roll{w}"] = df.groupby("practice_id")["paid"].transform(
            lambda s: s.rolling(w, min_periods = 1).mean()
        )

    df["dow"] = df["d"].dt.weekday
    df["month_num"] = df["d"].dt.month
    return df