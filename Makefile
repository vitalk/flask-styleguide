clean:
	@find . -name *.py? -delete


test:
	@python setup.py test --coverage


install:
	@pip install -r requirements.txt


.PHONY: clean test install
