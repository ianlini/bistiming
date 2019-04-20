BisTiming
=========
.. image:: https://img.shields.io/travis/ianlini/bistiming/master.svg
   :target: https://travis-ci.org/ianlini/bistiming
.. image:: https://img.shields.io/pypi/v/bistiming.svg
   :target: https://pypi.org/project/bistiming/
.. image:: https://img.shields.io/pypi/l/bistiming.svg
   :target: https://pypi.org/project/bistiming/

A logging-friendly timing module for Python.

When we search the stopwatch or timing module for Python on the internet, we can find a
lot of code snippets, but none of them is powerful or convenient enough to do our daily
jobs.
BisTiming aims at implementing all the missing functions in those code snippets and
preventing us from reinventing the wheel.
It is very useful when you want to log something with some timing information or even
optimize the performance of your code.

Installation
------------
.. code:: bash

   pip install bistiming

Getting started
---------------

BisTiming has a context manager interface that let you log the running time of a block
easily, and it also has low-level APIs that let you time multiple segments or loops of
code easily.

See `examples/stopwatch_examples.py <examples/stopwatch_examples.py>`_ for all the useful
examples of ``Stopwatch``.

Low-level API
++++++++++++++++++++++

Context manager
++++++++++++++++++++++

API reference
-------------

Testing
-------

* Linter: ``flake8``.
* For the current environment: ``python setup.py test``.
* For Python 2.7, 3.5, 3.6, 3.7, flake8 and installation test: ``tox``.
