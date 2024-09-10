.PHONY: all clean build test upload upload-test install install-dev lint format check

all: clean build upload

clean:
	rm -rf build dist *.egg-info

build:
	python setup.py sdist bdist_wheel

test:
	python -m pytest tests/

upload:
	twine upload dist/*

upload-test:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

lint:
	flake8 aicli tests

format:
	black aicli tests

check: lint test
