import sqlite3, pandas as pd
from .config import DB_PATH, RAW_DIR 
from .utils import ensure_dirs get_logger

log = get_logger("db")

def run_sql(con, sql_text: str):
    cur = con.cursor()
    cur.executescript(sql_text)
    con.commit()

def main():
    ensure_dirs(DB_PATH.parent)
    con = sqlite3.connect(DB_PATH)

    ddl = (Path("sql") / "ddl.sql").read_text()
    run_sql(con, ddl)

    claims = pd.read_csv(RAW_DIR / "claims.csv")
    cal = pd.read_csv(RAW_DIR / "calendar.csv")
    claims.to_sql("claims", con, if_exists = "replace", index = False)
    cal.to_sql("calendar", con, if_exists = "replace", index = False)

    run_sql(con, ddl)
    con.close()
    log.info("Loaded claims & calendar into %s", DB_PATH)

if __name__ = "__main__":
    from pathlib import Path 
    main()