.PHONY: tests cov htmlcov pep8 pylint docs dev-deps test-deps publish coveralls

tests:
	python mando/tests/run.py

cov:
	coverage erase && coverage run --include "mando/*" --omit "mando/tests/*,mando/napoleon/*" mando/tests/run.py
	coverage report -m

htmlcov: cov
	coverage html

pep8:
	pep8 mando --exclude "tests"

pylint:
	pylint --rcfile pylintrc mando

docs:
	cd docs && make html

dev-deps:
	pip install -r dev_requirements.pip

test-deps:
	pip install -r test_requirements.pip

publish:
	python setup.py sdist bdist_wheel upload

coveralls: test-deps cov
	coveralls
