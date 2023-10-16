.PHONY: all format lint help

all: help
	
format:
	poetry run ruff --select I --fix .

lint:
	poetry run ruff .

help:
	@echo '----'
	@echo 'lint                - run linters'
	@echo 'format              - run formatters'
