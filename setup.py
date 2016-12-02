#!/usr/bin/env python
import os
from setuptools import setup


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
    version="0.1.1",
    description='A timing and progress bar module for Python.',
    long_description=("See `github <https://github.com/ianlini/bistiming>`_ "
                      "for more information."),
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
