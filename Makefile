install:
	poetry install

build:
	poetry build

#delete this
run:
	poetry run page-loader https://page-loader.hexlet.repl.co/ -o var/tmp

package-install:
	python3 -m pip install --user dist/*.whl

lint:
	poetry run flake8 page_loader tests

test:
	poetry run pytest

test-coverage-report:
	poetry run pytest --cov=page_loader --cov-report xml tests/

test-coverage:
	poetry run pytest --cov=page_loader