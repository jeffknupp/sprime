.PHONY: test,build,clean,docs

build: clean
	virtualenv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

test: build
	PYTHONPATH=`pwd`:${PYTHONPATH} py.test --cov=sandman --strict --verbose tests && \
	coverage html

docs: build
	PYTHONPATH=`pwd`:${PYTHONPATH} && cd docs && make html

test-full:
	pylint --rcfile=.pylintrc sandman

clean:
	rm -rf htmlcov
	rm -rf docs/_build
