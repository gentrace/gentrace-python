.PHONY: all clean format lint test tests test_watch integration_tests help

all: help
	
format:
	poetry run black .
	poetry run ruff --select I --fix .

lint:
	poetry run mypy .
	poetry run black . --check
	poetry run ruff .

help:
	@echo '----'
	@echo 'lint                - run linters'
