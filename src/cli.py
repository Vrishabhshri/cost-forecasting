import argparse
from .generate_mock import main as gen_mock
from .build_calendar import main as gen_cal
from .load_to_db import main as load_db
from .build_mart import main as build_mart
from .backtest import main as run_backtest
from .forecast import main as run_forecast
from .alerts import main as run_alerts

def main():
    p = argparse.ArgumentParser(description = "Cost Forecasting pipeline")
    p.add_argument("step", choices = [
        "generate-mock", "build-calendar", "load-db", "build-mart", "backtest", "forecast",
        "alerts", "all"
    ])
    args = p.parse_args()
    if args.step in ("generate-mock", "all"): gen_mock()
    if args.step in ("build-calendar","all"): gen_cal()
    if args.step in ("load-db","all"): load_db()
    if args.step in ("build-mart","all"): build_mart()
    if args.step in ("backtest","all"): run_backtest()
    if args.step in ("forecast","all"): run_forecast()
    if args.step in ("alerts","all"): run_alerts()

if __name__ == "__main__":
    main()