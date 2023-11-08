.DEFAULT_GOAL := install

PACKAGE_NAME=ome_zarr_pydantic
LINE_LENGTH=99

PATHS_TO_FORMAT=.

install:
	 #$(MAKE) format-check
	 #$(MAKE) lint
	 #$(MAKE) test
	poetry install

format:
	black --line-length=${LINE_LENGTH} ${PATHS_TO_FORMAT}
	isort --profile black ${PATHS_TO_FORMAT}

format-check:
	black --check --line-length=${LINE_LENGTH} --preview ${PATHS_TO_FORMAT}
	isort --check-only --profile black ${PATHS_TO_FORMAT}

lint:
	#mypy ${PATHS_TO_FORMAT}
	ruff check ${PATHS_TO_FORMAT}