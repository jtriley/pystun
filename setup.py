import os.path
from setuptools import setup, find_packages

import stun


def main():
    src = os.path.realpath(os.path.dirname(__file__))
    with open(os.path.join(src, 'README.rst'), encoding='utf-8') as fobj:
        readme = fobj.read()

    setup(
        name='pystun',
        version=stun.__version__,
        packages=find_packages(),
        zip_safe=False,
        license='MIT',
        author='Justin Riley (original author: gaohawk)',
        author_email='justin.t.riley@gmail.com',
        url='http://github.com/jtriley/pystun',
        description='A Python STUN client for getting NAT type and external IP (RFC 3489)',
        long_description=readme,
        long_description_content_type='text/x-rst',
        keywords='STUN NAT',
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.12',
            'Programming Language :: Python :: 3.13',
            'Programming Language :: Python :: 3.14',
            'Topic :: Internet',
            'Topic :: System :: Networking :: Firewalls',
        ],
        python_requires='>=3.9',
        entry_points={
            'console_scripts': [
                'pystun=stun.cli:main'
            ]
        }
    )


if __name__ == '__main__':
    main()
