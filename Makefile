.PHONY: clean build test_deploy deploy test

clean:
	rm -rf build dist *.egg-info

build:
	python setup.py sdist bdist_wheel

test_deploy: clean build
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*	

deploy: clean build
	twine upload dist/*

test:
	python -m pytest tests/*
