#!/usr/bin/env python
import os
from setuptools import setup, find_packages

src = os.path.realpath(os.path.dirname(__file__))

README = open(os.path.join(src, 'README.rst')).read()

setup(
    name='pystun',
    version="0.0.5",
    packages=find_packages(),
    scripts=['bin/pystun'],
    zip_safe=False,
    license='MIT',
    author='Justin Riley (original author: gaohawk)',
    author_email='justin.t.riley@gmail.com',
    url="http://github.com/jtriley/pystun",
    description="A Python STUN client for getting NAT type and external IP (RFC 3489)",
    long_description=README,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Internet",
        "Topic :: System :: Networking :: Firewalls",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
)
