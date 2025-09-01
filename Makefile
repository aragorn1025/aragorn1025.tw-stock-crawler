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

run:
	docker compose exec tw-stock-crawler \
		poetry run python src/main.py \
			--stock_numbers ${STOCK_NUMBERS} \
			$(if ${YEAR},--year ${YEAR}) \
			$(if ${MONTHS},--months ${MONTHS})
.PHONY: run
.SILENT: run

down:
	docker compose down
.PHONY: down
