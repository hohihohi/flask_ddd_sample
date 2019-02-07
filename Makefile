ROOT_DIR := .
PYTHON_FILES = $(find $(ROOT_DIR) -type f -name "*.py")

lint:
	pipenv run flake8 --show-source --statistics --ignore E501 $(PYTHON_FILES)
autopep8:
	pipenv run autopep8 -i --aggressive -r $(ROOT_DIR)
debug:
	pipenv run python -m ipdb $(PYTHON_FILE)
sort:
	pipenv run isort -rc $(PYTHON_FILES)

