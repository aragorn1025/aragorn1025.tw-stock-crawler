install:
	poetry install
.PHONY: install

lint:
	poetry run isort src/
	poetry run black src/
	poetry run flake8 src/
	poetry run pylint src/
.PHONY: lint

clean:
	poetry env remove --all
.PHONY: clean

build:
	docker compose build
.PHONY: build

up:
	docker compose up
.PHONY: up

OUTPUT ?= data/output.csv

run:
	docker compose exec tw-stock-crawler \
		poetry run python src/main.py \
			--stock_numbers ${STOCK_NUMBERS} \
			--year ${YEAR} \
			--output ${OUTPUT}
.PHONY: run

down:
	docker compose down
.PHONY: down
