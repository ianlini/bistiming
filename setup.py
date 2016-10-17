#!/usr/bin/env python
import os
from setuptools import setup

from bistiming import __version__

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
    install_requires = []

setup(
    name='bistiming',
    version=__version__,
    description='A timing and progress bar module for Python.',
    long_description='A timing and progress bar module for Python.',
    author='ianlini',
    url='https://github.com/ianlini/bistiming',
    setup_requires=setup_requires,
    install_requires=install_requires,
    classifiers=[
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
    test_suite='nose.collector',
    packages=[
        'bistiming',
    ],
    package_dir={
        'bistiming': 'bistiming',
    },
)
