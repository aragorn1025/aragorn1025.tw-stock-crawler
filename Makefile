install:
	poetry install
.PHONY: install

lint:
	poetry run isort src/
	poetry run black src/
	poetry run flake8 src/
	poetry run pylint src/
.PHONY: lint
