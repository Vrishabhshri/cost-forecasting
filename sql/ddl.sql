CREATE TABLE IF NOT EXISTS claims (
    claim_id TEXT PRIMARY KEY,
    patient_id INTEGER NOT NULL,
    service_date TEXT NOT NULL,
    practice_id TEXT NOT NULL,
    provider_id TEXT NOT NULL,
    cpt_code TEXT NOT NULL,
    units INTEGER NOT NULL CHECK (units > 0),
    charge_amount NUMERIC NOT NULL CHECK (charge_amount >= 0),
    paid_amount NUMERIC NOT NULL CHECK (paid_amount >= 0),
    denial_flag INTEGER NOT NULL,
    payer TEXT NOT NULL CHECK (payer in ('COMM', 'MEDICARE', 'MEDICAID')),
    place_of_service TEXT NOT NULL
);

CREATE INDEX claims_service_practice_idx ON claims (service_date, practice_id);

CREATE TABLE calendar (
    date TEXT PRIMARY KEY,
    is_weekend INTEGER NOT NULL CHECK (is_weekend in (0, 1)),
    month INTEGER NOT NULL CHECK (month BETWEEN 1 AND 12),
    year INTEGER NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    iso_week INTEGER NOT NULL CHECK (iso_week BETWEEN 1 AND 53),
    is_holiday INTEGER NOT NULL CHECK (is_holiday in (0, 1)),
    flu_season_flag INTEGER NOT NULL CHECK (flu_season_flag in (0, 1)),
    end_of_month_flag INTEGER NOT NULL CHECK (end_of_month_flag in (0, 1))
);