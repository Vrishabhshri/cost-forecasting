import pandas as pd, holidays as pyhol, numpy as np
from .config import RAW_DIR, START_DATE, END_DATE
from .utils import ensure_dirs, get_logger 

log = get_logger("calendar")

def build_calendar(start = START_DATE, end = END_DATE, country = "US"):

    idx = pd.date_range(start, end, freq = "D")
    us_hol = pyhol.UnitedStates() if country == "US" else pyhol.CountryHoliday(country)

    df = pd.DataFrame({"date": idx.date})

    df["is_weekend"] = (idx.weekday >= 5).astype(int)
    df["month"] = idx.month 
    df["year"] = idx.year
    df["iso_week"] = idx.isocalendar().week.astype(int)
    df["is_holiday"] = np.array([int(d in us_hol) for d in df["date"]], dtype = int)
    df["flu_season_flag"] = np.isin(idx.month, [1, 2, 3, 11, 12]).astype(int)
    df["end_of_month_flag"] = (idx.is_month_end).astype(int)
    df["date"] = df["date"].astype(str)
    return df

def main():
    ensure_dirs(RAW_DIR)
    cal = build_calendar()
    out = RAW_DIR / "calendar.csv"
    cal.to_csv(out, index = False)
    log.info("Wrote %s (%d rows)", out, len(cal))

if __name__ == "__main__":
    main()