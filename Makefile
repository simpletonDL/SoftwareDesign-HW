run:
	python3 bash.py

test:
	pytest

requirements:
	pip3 install -r src/requirements.txt
	pip3 install -r testing/requirements.txt

pylint:
	pylint --rcfile .pylintrc src