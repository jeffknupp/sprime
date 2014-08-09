.PHONY: test,build,clean

build: clean
	virtualenv venv && \
	source venv/bin/activate && \
	pip install -r requirements.txt

test: build
	PYTHONPATH=`pwd`:${PYTHONPATH} py.test --cov=sandman --strict --verbose tests && \
	coverage html

clean:
	rm -rf htmlcov
