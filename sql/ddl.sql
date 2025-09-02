CREATE TABLE IF NOT EXISTS claims (
    claim_id VARCHAR(32) PRIMARY KEY,
    patient_id BIGINT NOT NULL,
    service_date DATE NOT NULL,
    practice_id VARCHAR(16) NOT NULL,
    provider_id VARCHAR(16) NOT NULL,
    cpt_code CHAR(5) NOT NULL,
    units SMALLINT NOT NULL CHECK (units > 0),
    charge_amount NUMERIC(10, 2) NOT NULL CHECK (charge_amount >= 0),
    paid_amount NUMERIC(10, 2) NOT NULL CHECK (paid_amount >= 0),
    denial_flag BOOLEAN NOT NULL,
    payer VARCHAR(16) NOT NULL CHECK (payer in ('COMM', 'MEDICARE', 'MEDICAID')),
    place_of_service VARCHAR(32) NOT NULL
);

CREATE INDEX claims_service_practice_idx ON claims (service_date, practice_id);
CREATE INDEX claims_practice_idx ON claims (practice_id, service_date);
CREATE INDEX claims_payer_idx ON claims (payer);
CREATE INDEX claims_cpt_idx ON claims (cpt_code);

CREATE TABLE calendar (
    date DATE PRIMARY KEY,
    is_weekend BOOLEAN NOT NULL,
    month SMALLINT NOT NULL CHECK (month BETWEEN 1 AND 12),
    year SMALLINT NOT NULL CHECK (year BETWEEN 1900 AND 2100),
    iso_week SMALLINT NOT NULL CHECK (iso_week BETWEEN 1 AND 53),
    is_holiday BOOLEAN NOT NULL DEFAULT FALSE,
    flu_season_flag BOOLEAN NOT NULL DEFAULT FALSE,
    end_of_month_flag BOOLEAN NOT NULL DEFAULT FALSE
);