all: test

test:
	python -m unittest

dep:
	python -m pip install -r requirements.txt

install:
	python -m pip install -e .

