.PHONY: test_deploy deploy

test_deploy:
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*	

deploy:
	twine upload dist/*

