install:
	poetry install
.PHONY: install

lint:
	poetry run isort .
	poetry run black .
	poetry run flake8 .
	poetry run pylint src/
.PHONY: lint
