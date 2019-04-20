BisTiming
=========
.. image:: https://img.shields.io/travis/ianlini/bistiming/master.svg
   :target: https://travis-ci.org/ianlini/bistiming
.. image:: https://img.shields.io/pypi/v/bistiming.svg
   :target: https://pypi.org/project/bistiming/
.. image:: https://img.shields.io/pypi/l/bistiming.svg
   :target: https://pypi.org/project/bistiming/

A logging-friendly timing module for Python.

Installation
------------
.. code:: bash

   pip install bistiming

Examples
--------

* See `examples/stopwatch_examples.py <examples/stopwatch_examples.py>`_ for the examples of ``Stopwatch``.
* The output of executing ``python examples/stopwatch_examples.py``:

  .. image:: examples/simple_timing_example.gif

Testing
-------

* Linter: ``flake8``.
* For the current environment: ``python setup.py test``.
* For Python 2.7, 3.5, 3.6, 3.7, flake8 and installation test: ``tox``.
