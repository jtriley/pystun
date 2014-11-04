TESTPATH=./tests

.PHONY: all check test unittest

all: test

test: check unittest

check:
	prospector

unittest:
	nosetests --with-coverage --cover-package=stun --cover-inclusive $(TESTPATH)
