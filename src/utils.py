from pathlib import Path 
import logging

def ensure_dirs(*paths: Path):
    for p in paths:
        p.mkdir(parents = True, exist_ok = True)

def get_logger(name = "app"):
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s %(levelname)s %(message)s"
    )

    return logging.getLogger(name)