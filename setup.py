#!/usr/bin/env python
import os
from setuptools import setup, find_packages


on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
# read the docs could not compile numpy and c extensions
if on_rtd:
    setup_requires = []
    install_requires = []
else:
    setup_requires = [
        'nose',
        'coverage',
    ]
    install_requires = [
        'six',
    ]

setup(
    name='bistiming',
    version="0.2.0",
    description='A timing and progress bar module for Python.',
    long_description=("See `github <https://github.com/ianlini/bistiming>`_ "
                      "for more information."),
    author='ianlini',
    url='https://github.com/ianlini/bistiming',
    setup_requires=setup_requires,
    install_requires=install_requires,
    license="BSD 2-Clause",
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    test_suite='nose.collector',
    packages=find_packages(exclude=('examples', 'examples.*')),
)
