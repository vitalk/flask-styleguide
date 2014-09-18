clean:
	@find . -name *.py? -delete


test:
	@python setup.py test --coverage


install:
	@python setup.py install


.PHONY: clean test install
