import os.path
from setuptools import setup, find_packages

import stun


def main():
    src = os.path.realpath(os.path.dirname(__file__))
    README = open(os.path.join(src, 'README.rst')).read()

    setup(
        name='pystun',
        version=stun.__version__,
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
        ],
    )

if __name__ == '__main__':
    main()
