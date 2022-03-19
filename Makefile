init:
	pip3 install -e ".[testing]"

test: clean init
	python3 setup.py --verbose test
	python3 -m pylint colima_helper/ test/

test-e2e: clean init
	cd tmp/test-basic;colima-helper --list

clean:
	find . -name "__pycache__" | xargs rm -r
