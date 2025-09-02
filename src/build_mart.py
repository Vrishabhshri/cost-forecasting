import sqlite3, pandas as pd 
from pathlib import Path 
from .config import DB_PATH, CURATED_DIR
from .utils import ensure_dirs, get_logger

log = get_logger("mart")

def main():
    ensure_dirs(CURATED_DIR)
    sql = (Path("sql") / "mart_daily.sql").read_text()
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, con)
    out = CURATED_DIR / "mart_daily.csv"
    df.to_csv(out, index = False)
    con.close()
    log.info("Wrote mart %s (%d rows)", out, len(df))

if __name__ == "__main__":
    main()