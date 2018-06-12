Changelog
---------
1.0.0 (2018/06/12)
******************
- Release as ``pystun3`` with support for Python 3.

0.1.0 (2014/11/07)
******************
- Drop support for Python 2.6 and earlier.
- Add a proper LICENSE file.
- Build the project via Travis CI.
- Add a Makefile to orchestrate the build.
- Install infrastructure to write and run unit tests with coverage reporting.
- Move changelog to separate file.
- Perform static code analysis via prospector.
- Drop pep8 and pyflakes scripts, as superseeded.
- Drop ez_script.
- Suggest installing via pip. Deprecate easy_install.
- Bring the setup script up-to-scratch with pyroma.
- Drop redundant pystun script and set stun.cli:main as entry point.
- Install initial support for building a universal wheel.
- Update list of STUN servers.
- Drop optparse in favour of argparse.
- Update usage message in README.

0.0.4 (2013/10/14)
******************
- Stun: added functionality to pass the initial STUN server port explicitly

0.0.3 (2013/05/21)
******************
- Stun: fix UnboundLocalError in get_nat_type.
- Stun: remove dead hosts from stun server list.
- Handling get address info error.
- Add version info to stun module and stun.cli.
- Add MANIFEST.in and include README.rst.
