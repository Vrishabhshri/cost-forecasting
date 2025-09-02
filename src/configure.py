from pathlib import Path 

DATA_DIR = Path("data")
RAW_DIR = DATA_DIR / "raw"
CURATED_DIR = DATA_DIR / "curated"
DB_PATH = DATA_DIR / "claims.db"

METRICS_DIR = Path("metrics")
MODELS_DIR = Path("models")

START_DATE = "2022-01-01"
END_DATE = "2024-12-31"

FORECAST_HORIZON_DAYS = 28
RANDOM_SEED = 42