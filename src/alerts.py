import numpy as np, pandas as pd 
from .config import CURATED_DIR
from .utils import get_logger 

log = get_logger("alerts")

def compute_alerts(forecast_csv = "forecast_export.csv", threshold = 15.0):
    df = pd.read_csv(CURATED_DIR / forecast_csv, parse_dates = ["d"])
    hist = df[df["is_forecast"] == 0].copy()
    hist["trail7"] = hist.groupby("practice_id")["yhat"].transform(lambda s: s.rolling(7, 1).mean())
    hist["abs_pct_err_vs_trail"] = 100 * abs(hist["yhat"] - hist["trail7"]) / hist["trail7"].clip(lower = 1e-8)
    recent = hist.groupby("practice_id").tail(14)
    agg = recent.groupby("practice_id")["abs_pct_err_vs_trail"].mean().reset_index()
    agg["volatility_alert"] = agg["abs_pct_err_vs_trail"] > threshold 
    return agg

def main():
    alerts = compute_alerts()
    out = CURATED_DIR / "alerts.csv"
    alerts.to_csv(out, index = False)
    log.info("Wrote %s", out)

if __name__ == "__main__":
    main()