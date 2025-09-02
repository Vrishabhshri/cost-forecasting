import numpy as np, pandas as pd 
from datetime import datetime 
rng = np.random_default_rng(42)

start, end = "2022-01-01", "2024-12-31"
dates = pd.date_range(start, end, freq="D")

practices = ["PRA1", "PRA2", "PRA3"]
cpts = ["99213","99214","93000","70450","36415"]

rows = []
for d in dates:

    dow = d.weekday()
    year_factor = 1 + 0.08 * ((d.year - 2022) / 3)
    season = 1 + 0.15 * np.sin(2 * np.pi * (d.timetuple().tm_yday) / 365.25)
    weekseason = 1 + 0.07 * (1 if dow in (1, 2) else -0.5 if dow == 5 else 0)
    flu = 1 + (0.12 if d.month in (1, 2, 3, 11, 12) else 0)

    for pr in practices:

        base_vol = 25 if pr == "PRA1" else 18 if pr == "PRA2" else 12
        day_vol = rng.poisson(lam = base_vol * year_factor * weekseason * flu)

        for _ in range(day_vol):

            cpt = rng.choice(cpts, p = [0.3, 0.3, 0.15, 0.15, 0.1])
            units = 1 if cpt != "36415" else rng.integers(1, 3)
            charge = {"99213": 120, "99214": 180, "93000": 70, "70450": 650, "36415": 20}[cpt] * units
            payer = rng.choice(["COMM", "MEDICARE", "MEDICAID"], p = [0.55, 0.3, 0.15])
            denial = rng.random() < (0.06 if payer = "COMM" else 0.08 if payer == "MEDICARE" else 0.12)
            paid = 0 if denial else charge * rng.uniform(0.5, 0.9)
            rows.append([f"C{rng.integers(10**9)}", rng.integers(10**7), d, pr, f"PROV{rng.integers(200)}",
                        cpt, units, round(charge, 2), round(paid, 2), int(denial), payer, "OFFICE"])
            
claims = pd.DateFrame(rows, columns = ["claim_id", "patient_id", "service_date", "practice_id", "provider_id", "cpt_code",
                                        "units", "charge_amount", "paid_amount", "denial_flag", "payer", "place_of_service"])

claims.to_csv("data/raw/claims.csv", index=False)