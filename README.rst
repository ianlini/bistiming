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

A logging-friendly timing module for Python.

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

See `examples/stopwatch_examples.py <https://github.com/ianlini/bistiming/blob/master/examples/stopwatch_examples.py>`_
for all the useful examples of ``Stopwatch``.

In the following guide, we assume that each line of code is executed immediately
after the previous one finished.
We use ``sleep()`` to simulate the running time of the program we want to evaluate.

Context Manager
+++++++++++++++

The simplest way to use BisTiming is simply using a ``with Stopwatch():`` to include the code
we want to evaluate:

>>> from bistiming import Stopwatch
>>> from time import sleep
>>> with Stopwatch():
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
...
do something
finished something
... done in 0:00:00.100229

The stopwatch output ``...`` when entering the ``with``-block, and output
``... done in...`` when exiting.

If we want to add more description to describe what we are doing, we can use the first
parameter in ``Stopwatch()``:

>>> with Stopwatch("Waiting"):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
...Waiting
do something
finished something
...Waiting done in 0:00:00.100330

``Waiting`` is added immediately after the prefix ``...``.

If we don't want to output anything when entering the block, we can use the parameter
``verbose_start``:

>>> with Stopwatch("Waiting", verbose_start=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
do something
finished something
...Waiting done in 0:00:00.100333

Similarly, if we don't want to output anything when exiting the block, we can use the
parameter ``verbose_end``:

>>> with Stopwatch("Waiting", verbose_end=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
...Waiting
do something
finished something

If don't want any output, we can use the parameter ``verbose`` to turn off all of them:

>>> with Stopwatch(verbose=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
do something
finished something

Sometimes we only want to see one line for both entering and exiting.
We can use the parameter ``end_in_new_line``:

>>> with Stopwatch("Waiting", end_in_new_line=False):
...     sleep(0.1)
...
...Waiting done in 0:00:00.100340

This will output ``...Waiting`` first, and when exiting the block, ``done in...``
will be appended after that line.

If you don't like the default prefix ``...``, you can use the parameter ``prefix`` to
replace it:

>>> with Stopwatch("Waiting", prefix="[bistiming] "):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
[bistiming] Waiting
do something
finished something
[bistiming] Waiting done in 0:00:00.100323

The built-in module ``logging`` is very useful when we are developing a complicated
service.
We can use the parameter ``logger`` to tell the stopwatch to output using a logger:

>>> import logging
>>> logging.basicConfig(
...     level=logging.DEBUG,
...     format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
>>> logger = logging.getLogger(__name__)
>>> with Stopwatch("Waiting", logger=logger):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
[2019-04-24 22:27:52,244] INFO: __main__: ...Waiting
do something
finished something
[2019-04-24 22:27:52,345] INFO: __main__: ...Waiting done in 0:00:00.100326

We can also configure the logging level using the parameter ``logging_level``:

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
[datetime.timedelta(microseconds=100468), datetime.timedelta(microseconds=100440)]
>>> timer.get_cumulative_elapsed_time()
datetime.timedelta(microseconds=200908)

Each item in ``split_elapsed_time`` is the running time of the code segment in each
iteration, and we can use ``get_cumulative_elapsed_time()`` to get the total running
time of that segment.

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

When using the low-level API, we first initialize a stopwatch (we have talked a lot
about the initialization in the `context manager <#context-manager>`_ section):

>>> from time import sleep
>>> from bistiming import Stopwatch
>>> timer = Stopwatch("Waiting")
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00
Elapsed time: 0:00:00

The output of ``log_elapsed_time()`` is ``0:00:00`` because we haven't started the
stopwatch.

Now we start the stopwatch using ``start()``:

>>> timer.start()
...Waiting
<bistiming.stopwatch.Stopwatch object at 0x7f0d90000a90>
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00.1
Elapsed time: 0:00:00.101331
>>> timer.get_elapsed_time()  # 0:00:00.1
datetime.timedelta(microseconds=101944)

After 0.1s sleeping, we log the elapsed time.
The log is not exactly 0.1s because there are some overhead between the starting time
and logging time.
``get_elapsed_time()`` returns a `datetime.timedelta <https://docs.python.org/3/library/datetime.html#datetime.timedelta>`_
object instead of printing.

Now we pause the timer using ``pause()`` after 0.1s more sleeping:

>>> sleep(0.1)
>>> timer.pause()
>>> timer.log_elapsed_time()  # 0:00:00.2
Elapsed time: 0:00:00.202967
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00.2
Elapsed time: 0:00:00.202967

After pausing, the elapsed time remains exactly the same.

Now we introduce the splitting function, ``split()``, which stores the running time of the
current split and restarts the stopwatch:

>>> timer.split()  # 0:00:00.2
...Waiting done in 0:00:00.202967
>>> timer.log_elapsed_time()  # 0:00:00
Elapsed time: 0:00:00
>>> timer.get_cumulative_elapsed_time()  # 0:00:00.2
datetime.timedelta(microseconds=202967)

By default, ``start()`` and ``split()`` will output some logs.
They both have a ``verbose`` parameter to control whether to output.
If not set, they will use ``verbose_start`` and ``verbose_end`` defined during
initialization (``Stopwatch(verbose_start=True, verbose_end=True)``).
We can also use ``Stopwatch(verbose=False)`` to turn off all the output.

After splitting, the elapsed time is reset to 0.
There is also a convenient method ``get_cumulative_elapsed_time()`` that can return
the total running time of all splits (including the currently running one).
Now we start the stopwatch again:

>>> sleep(0.1)
>>> timer.start()
...Waiting
<bistiming.stopwatch.Stopwatch object at 0x7f0d90000a90>
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00.1
Elapsed time: 0:00:00.101195
>>> timer.get_cumulative_elapsed_time()  # 0:00:00.3
datetime.timedelta(microseconds=304858)

We can see that ``get_cumulative_elapsed_time()`` also increases.

Let's try to split more:

>>> timer.split()  # 0:00:00.1
...Waiting done in 0:00:00.102339
>>> sleep(0.1)
>>> timer.pause()
>>> timer.split()  # 0:00:00.1
...Waiting done in 0:00:00.101126
>>> timer.get_cumulative_elapsed_time()  # 0:00:00.4
datetime.timedelta(microseconds=406432)
>>> timer.split_elapsed_time  # [0:00:00.2, 0:00:00.1, 0:00:00.1]
[datetime.timedelta(microseconds=202967),
 datetime.timedelta(microseconds=102339),
 datetime.timedelta(microseconds=101126)]

If we split without pausing, the stopwatch will keep running, so the second ``split()``
got 0.1s.
Currently, we have split 3 times.
We can use ``timer.split_elapsed_time`` to see the running time of the 3 splits.

The last thing we have not mentioned is ``reset()``:

>>> timer.reset()
>>> timer.log_elapsed_time()  # 0:00:00
Elapsed time: 0:00:00
>>> timer.get_cumulative_elapsed_time()  # 0:00:00
datetime.timedelta(0)
>>> timer.split_elapsed_time  # []
[]
>>> sleep(0.1)
>>> timer.start()
...Waiting
<bistiming.stopwatch.Stopwatch object at 0x7f0d90000a90>
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00.1
Elapsed time: 0:00:00.10137

``reset()`` will clear all the states in the stopwatch just like a whole new stopwatch.

Documentation
-------------
See the `documentation <https://bistiming.readthedocs.io>`_ for more information.
