import numpy as np, pandas as pd 
from datetime import datetime 
from .config import RAW_DIR, START_DATE, END_DATE, RANDOM_SEED 
from .utils import ensure_dirs, get_logger 

log = get_logger("mock")

def generate_claims(start = START_DATE, end = END_DATE):
    rng = np.random.default_rng(RANDOM_SEED)
    dates = pd.date_range(start, end, freq = "D")
    practices = ["PRA1", "PRA2", "PRA3"]
    cpts = ["99213","99214","93000","70450","36415"]

    rows = []
    for d in dates:

        dow = d.weekday()
        year_factor = 1 + 0.06 * ((d.year - pd.Timestamp(start).year) / 3)
        season = 1 + 0.15 * np.sin(2 * np.pi * (d.dayofyear) / 365.25)
        weekday = 1 + (0.08 if dow in (1, 2) else -0.05 if dow == 5 else 0.0)
        flu = 1 + (0.12 if d.month in (1, 2, 3, 11, 12) else 0)

        for pr in practices:

            base = 26 if pr == "PRA1" else 18 if pr == "PRA2" else 12
            vol = rng.poisson(lam = max(0.1, base * year_factor * season * weekday * flu))

            for _ in range(vol):

                cpt = rng.choice(cpts, p = [0.3, 0.3, 0.15, 0.15, 0.1])
                units = 1 if cpt != "36415" else rng.integers(1, 3)
                charge = {"99213": 120, "99214": 180, "93000": 70, "70450": 650, "36415": 20}[cpt] * units
                payer = rng.choice(["COMM", "MEDICARE", "MEDICAID"], p = [0.55, 0.3, 0.15])
                denial = int(rng.random() < (0.06 if payer == "COMM" else 0.08 if payer == "MEDICARE" else 0.12))
                paid = 0 if denial else charge * rng.uniform(0.5, 0.9)
                rows.append([f"C{rng.integers(10**9)}", rng.integers(10**7), d.date().isoformat(), pr, f"PROV{rng.integers(200)}",
                            cpt, int(units), round(charge, 2), round(paid, 2), int(denial), payer, "OFFICE"])
            
    df = pd.DataFrame(rows, columns = ["claim_id", "patient_id", "service_date", "practice_id", "provider_id", "cpt_code",
                                        "units", "charge_amount", "paid_amount", "denial_flag", "payer", "place_of_service"])

    return df

def main():
    ensure_dirs(RAW_DIR)
    df = generate_claims()
    out = RAW_DIR / "claims.csv"
    df.to_csv(out, index = False)
    log.info("Wrote %s (%d rows)", out, len(df))

if __name__ == "__main__":
    main()