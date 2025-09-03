.PHONY: all mock calendar db mart backtest forecast alerts clean

all: mock calendar db mart backtest forecast alerts

mock:
	python -m src.cli generate-mock

calendar:
	python -m src.cli build-calendar

db:
	python -m src.cli load-db

mart:
	python -m src.cli build-mart

backtest:
	python -m src.cli backtest

forecast:
	python -m src.cli forecast

alerts:
	python -m src.cli alerts

clean:
	rm -f data/claims.db
	rm -rf data/raw/*.csv data/curated/*.csv metrics/*.csv
