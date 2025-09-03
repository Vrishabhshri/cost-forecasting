import numpy as np, pandas as pd 
from pathlib import Path 
from statsmodels.tsa.statespace.sarimax import SARIMAX 
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import TimeSeriesSplit
from .features import add_time_features
from .metrics import mape, smape, wape
from .config import CURATED_DIR, METRICS_DIR 
from .utils import ensure_dirs, get_logger

log = get_logger("backtest")

def seasonal_naive(y: pd.Series, horizon: int):
    y = y.copy()
    shifted = y.shift(7)
    base = shifted.tail(horizon)
    if base.isna().any():
        last7 = y.tail(7)
        if len(last7) == 0:
            return np.repeat(y.iloc[-1] if len(y) else 0.0, horizon)
        repeats = int(np.ceil(horizon / 7))
        return np.tile(last7.values, repeats)[:horizon]
    return base.values

def rolling_backtest(df, horizon = 28):
    df = add_time_features(df)
    results = []
    for pr, g in df.groupby("practice_id"):
        g = g.dropna(subset = ["paid"]).sort_values("d")

        cutoff = g["d"].max() - pd.Timedelta(days = 180)
        train = g[g["d"] <= cutoff]
        test = g[g["d"] > cutoff]

        start_idx = 0
        exog_cols = ["dow", "is_holiday", "flu_season_flag", "paid_lag1", "paid_lag7", "paid_roll28"]

        while True:
            window = test.iloc[start_idx:start_idx + horizon]
            if len(window) < horizon: break

            up_to = pd.concat([train, test.iloc[:start_idx]], axis = 0)
            up_to = up_to.dropna(subset = ["paid_lag1", "paid_lag7", "paid_roll28"])

            if len(up_to) < 60:
                start_idx += horizon; continue

            mod = SARIMAX(
                up_to["paid"],
                order = (1, 1, 1),
                season_order = (0, 1, 1, 7),
                exog = up_to[exog_cols],
                enfore_stationarity = False,
                enforce_invertibility = False
            ).fit(disp = False)

            w = window.dropna(subset = exog_cols)
            if len(w) < horizon:
                start_idx += horizon; continue

            fc = mod.get_forecast(steps = horizon, exog = w[exog_cols])
            yhat = fc.predicted_mean.values 
            base = seasonal_naive(pd.concat([up_to["paid"], window["paid"]]), horizon)
            y = window["paid"].values[:horizon]

            results.append({
                "practice_id": pr,
                "window_start": window["d"].iloc[0],
                "window_end": window["d"].iloc[-1],
                "mape_sarimax": mape(y,yhat),
                "mape_seasonal": mape(y,base),
                "wape_sarimax": wape(y,yhat),
                "wape_seasonal": wape(y,base),
                "smape_sarimax": smape(y,yhat),
                "smape_seasonal": smape(y,base)
            })

            start_idx += horizon
            
        return pd.DataFrame(results)

def main():
    ensure_dirs(METRICS_DIR)
    df = pd.read_csv(CURATED_DIR / "mart_daily.csv", parse_dates = ["d"])
    bt = rolling_backtest(df)
    out = METRICS_DIR / "backtest.csv"
    bt.to_csv(out, index = False)
    log.info("Wrote %s", out)

if __name__ == "__main__":
    main()