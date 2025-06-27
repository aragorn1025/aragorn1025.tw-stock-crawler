install:
	poetry install
.PHONY: install

lint:
	poetry run isort .
	poetry run black .
	poetry run flake8 .
.PHONY: lint
