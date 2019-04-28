BisTiming
=========
.. image:: https://img.shields.io/travis/ianlini/bistiming/master.svg
   :target: https://travis-ci.org/ianlini/bistiming
.. image:: https://readthedocs.org/projects/pip/badge/
   :target: https://bistiming.readthedocs.io/
.. image:: https://img.shields.io/pypi/v/bistiming.svg
   :target: https://pypi.org/project/bistiming/
.. image:: https://img.shields.io/pypi/l/bistiming.svg
   :target: https://github.com/ianlini/bistiming/blob/master/LICENSE
.. image:: https://img.shields.io/github/stars/ianlini/bistiming.svg?style=social
   :target: https://github.com/ianlini/bistiming

A logging-friendly stopwatch and profiling tool for Python.

When we search the stopwatch or timing module for Python on the internet, we can find a
lot of code snippets, but none of them is powerful or convenient enough to do our daily
jobs.
BisTiming aims at implementing all the missing functions in those code snippets and
preventing us from reinventing the wheel.
It is very useful when we want to log something with some timing information or even
optimize the performance of our code.

This package is tested with Python 2.7, 3.5, 3.6 and 3.7, but may also work in other
Python versions.

.. contents::

Installation
------------
.. code:: bash

   pip install bistiming

Getting Started
---------------

BisTiming has a context manager interface that let us log the running time of a code block
easily, and it also has low-level API that let us time multiple segments or loops of
code easily.

See `examples <https://github.com/ianlini/bistiming/blob/master/examples/>`_
for all the useful examples.

Context Manager
+++++++++++++++

The simplest way to use BisTiming is using the context manager ``Stopwatch``
to include the code we want to evaluate:

>>> from bistiming import Stopwatch
>>> from time import sleep
>>> with Stopwatch("Waiting"):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
...Waiting
do something
finished something
...Waiting done in 0:00:00.100330

We can use the parameter `logger` and `logging_level` to tell the stopwatch to output
using a logger:

>>> import logging
>>> logging.basicConfig(
...     level=logging.DEBUG,
...     format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
>>> logger = logging.getLogger(__name__)
>>> with Stopwatch("Waiting", logger=logger, logging_level=logging.DEBUG):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
[2019-04-24 22:27:52,347] DEBUG: __main__: ...Waiting
do something
finished something
[2019-04-24 22:27:52,448] DEBUG: __main__: ...Waiting done in 0:00:00.100344

Another common use case is to evaluate the running time of a specific code segment
in a loop, we can initialize the stopwatch outside the loop, and reuse it in the loop:

>>> timer = Stopwatch("Waiting")
>>> for i in range(2):
...     with timer:
...         print("do something 1")
...         sleep(0.1)
...         print("finished something 1")
...     print("do something 2")
...     sleep(0.1)
...     print("finished something 2")
...
...Waiting
do something 1
finished something 1
...Waiting done in 0:00:00.100468
do something 2
finished something 2
...Waiting
do something 1
finished something 1
...Waiting done in 0:00:00.100440
do something 2
finished something 2
>>> timer.split_elapsed_time
[datetime.timedelta(microseconds=100468),
 datetime.timedelta(microseconds=100440)]
>>> timer.get_cumulative_elapsed_time()
datetime.timedelta(microseconds=200908)

Each item in ``split_elapsed_time`` is the running time of
the code segment in each iteration, and we can use
``get_cumulative_elapsed_time()``
to get the total running time of the code segment.

Low-level API
+++++++++++++
The low-level API is similar to a stopwatch in real life.
A simple use case using the low-level API is:

>>> from time import sleep
>>> from bistiming import Stopwatch
>>> timer = Stopwatch("Waiting").start()
...Waiting
>>> sleep(0.2)  # do the first step of my program
>>> timer.split()
...Waiting done in 0:00:00.201457
>>> sleep(0.1)  # do the second step of my program
>>> timer.split()
...Waiting done in 0:00:00.100982

The context manager

>>> with Stopwatch("Waiting"):
...     sleep(0.1)
...Waiting
...Waiting done in 0:00:00.100330

is actually equivalent to the low-level API:

>>> timer = Stopwatch("Waiting").start()
...Waiting
>>> sleep(0.1)
>>> timer.pause()
>>> timer.split()
...Waiting done in 0:00:00.100330

Advance Profiling
+++++++++++++++++
``MultiStopwatch`` in this package contains multiple
``Stopwatch``, so we can use them to define each code segment
we want to evaluate and compare easily:

>>> from time import sleep
>>> from bistiming import MultiStopwatch
>>> timers = MultiStopwatch(2, verbose=False)
>>> for i in range(5):
...    for i in range(2):
...       with timers[0]:
...             sleep(0.1)
...    with timers[1]:
...       sleep(0.1)
...
>>> timers.get_statistics()
{'cumulative_elapsed_time': [datetime.timedelta(seconds=1, microseconds=2879),
                             datetime.timedelta(microseconds=501441)],
 'percentage': [0.6666660019144863, 0.3333339980855137],
 'n_splits': [10, 5],
 'mean_per_split': [datetime.timedelta(microseconds=100288),
                    datetime.timedelta(microseconds=100288)]}

We can also use ``pandas.DataFrame`` to make the statistics more readable
(note that you may need to
`install pandas <https://pandas.pydata.org/pandas-docs/stable/install.html>`_ first):

>>> import pandas as pd
>>> pd.DataFrame(timers.get_statistics())
  cumulative_elapsed_time  percentage  n_splits  mean_per_split
0         00:00:01.002879    0.666666        10 00:00:00.100288
1         00:00:00.501441    0.333334         5 00:00:00.100288

Documentation
-------------
There are a lot more ways to use this package.
See the `documentation <https://bistiming.readthedocs.io>`_ for more information.
