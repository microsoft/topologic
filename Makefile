.PHONY: clean build init test test-report

SPHINX_OPTS=

setup-venv:
	python3 -m pip install virtualenv
	python3 -m virtualenv venv
	. ./venv/bin/activate
	python3 -m pip install -U pip setuptools wheel

init:
	pip install -r requirements.txt

build:
	python3 setup.py build sdist

lint:
	flake8 ./topologic ./tests

type-check:
	mypy ./topologic
	mypy ./tests

test: type-check run-test-report lint 

run-test-report:
	pytest tests topologic --doctest-modules --junit-xml=build/test-results.xml

test-report: type-check run-test-report lint

clean:
	rm -rf build dist topologic.egg-info
	find . -name __pycache__ -print0 | xargs -0 rm -r

doc:
	#sphinx-apidoc -f -M -o docs topologic
	sphinx-build -a docs/ docs/_build/html $(SPHINX_OPTS) 

