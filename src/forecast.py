import numpy as np, pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX 
from .features import add_time_features
from .config import CURATED_DIR, FORECAST_HORIZON_DAYS
from .utils import get_logger 

log = get_logger("forecast")

def fit_and_forecast_per_practice(df, horizon = FORECAST_HORIZON_DAYS):
    df = add_time_features(df)
    out_rows = []

    for pr, g in df.groupby("practice_id"):
        g = g.sort_values("d")
        exog_cols = ["dow", "is_holiday", "flu_season_flag", "paid_lag1", "paid_lag7", "paid_roll28"]
        g2 = g.dropna(subset = exog_cols + ["paid"]).copy()
        if len(g2) < 60:
            log.warning("Skipping %s (insufficient history)", pr)
            continue 
        mod = SARIMAX(
            g2["paid"], 
            order = (1, 1, 1), 
            seasonal_order = (0, 1, 1, 7),
            exog = g2[exog_cols], 
            enfore_stationarity = False, 
            enforce_invertibility = False
        ).fit(disp = False)

        tail = g2.tail(28)
        future_idx = pd.date_range(g["d"].max() + pd.Timedelta(days = 1), periods = horizon, freq = "D")

        cal_cols = ["dow", "is_holiday", "flu_season_flag"]
        cal_future = pd.DataFrame({"d": future_idx})
        cal_future["dow"] = cal_future["d"].dt.weekday
        cal_future["is_holiday"] = 0
        cal_future["flu_season_flag"] = cal_future["d"].dt.month.isin([1, 2, 3, 11, 12]).astype(int)
        
        last_paid = g2["paid"].values 
        cal_future["paid_lag1"] = np.tile(tail["paid"].values[-1], len(cal_future))
        cal_future["paid_lag7"] = np.tile(tail["paid"].values[-7:].mean(), len(cal_future))
        cal_future["paid_roll28"] = np.tile(g2["paid"].tail(28).mean(), len(cal_future))

        exog_future = cal_future[exog_cols]
        fc = mod.get_forecast(steps = horizon, exog = exog_future)
        pm = fc.predicted_mean
        ci = fc.conf_int(alpha = 0.2)

        for i, d in enumerate(future_idx):
            out_rows.append({
                "d": d.date().isoformat(),
                "practice_id": pr,
                "yhat": float(pm.iloc[i]),
                "pi_low": float(ci.iloc[i, 0]),
                "pi_high": float(ci.iloc[i, 1]),
                "is_forecast": 1
            })

        for _, r in g[["d", "practice_id", "paid"]].iterrows():
            out_rows.append({
                "d": pd.to_datetime(r["d"]).date().isoformat(),
                "practice_id": pr,
                "yhat": float(r["paid"]),
                "pi_low": None,
                "pi_high": None,
                "is_forecast": 0
            })

    return pd.DataFrame(out_rows)

def main():
    df = pd.read_csv(CURATED_DIR / "mart_daily.csv", parse_dates = ["d"])
    out = fit_and_forecast_per_practice(df)
    out = out.sort_values(["practice_id", "d"])
    out.to_csv((CURATED_DIR / "forecast_export.csv"), index = False)
    log.info("Wrote %s", (CURATED_DIR / "forecast_export.csv"))

if __name__ == "__main__":
    main()