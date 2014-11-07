BINPATH=./bin
STUNPATH=./stun
TESTPATH=./tests

.PHONY: all check test unittest

all: test

test: check unittest

check:
	prospector

unittest:
	nosetests --with-coverage --cover-package=stun --cover-inclusive $(TESTPATH)

clean:
	rm -rf pystun.egg-info
	$(RM) *.pyc *.pyo
	$(RM) $(BINPATH)/*.pyc $(BINPATH)/*.pyo
	$(RM) $(STUNPATH)/*.pyc $(STUNPATH)/*.pyo
	$(RM) $(TESTPATH)/*.pyc $(TESTPATH)/*.pyo
