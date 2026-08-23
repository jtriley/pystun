BINPATH=./bin
STUNPATH=./stun
TESTPATH=./tests

.PHONY: all check test unittest

all: test

test: check unittest

check:
	prospector

unittest:
	coverage run --source=$(STUNPATH) -m pytest $(TESTPATH)
	coverage report -m

clean:
	rm -rf pystun.egg-info
	$(RM) *.pyc *.pyo
	$(RM) $(BINPATH)/*.pyc $(BINPATH)/*.pyo
	$(RM) $(STUNPATH)/*.pyc $(STUNPATH)/*.pyo
	$(RM) $(TESTPATH)/*.pyc $(TESTPATH)/*.pyo
