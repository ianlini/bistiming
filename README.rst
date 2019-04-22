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
It is very useful when you want to log something with some timing information or even
optimize the performance of your code.

Installation
------------
.. code:: bash

   pip install bistiming

Getting Started
---------------

BisTiming has a context manager interface that let you log the running time of a code block
easily, and it also has low-level API that let you time multiple segments or loops of
code easily.

See `examples/stopwatch_examples.py <https://github.com/ianlini/bistiming/blob/master/examples/stopwatch_examples.py>`_
for all the useful examples of ``Stopwatch``.

Context Manager
+++++++++++++++

Low-level API
+++++++++++++
The low-level API is similar to a stopwatch in real life.
A simple use case using the low-level API is:

.. code-block:: python

   >>> timer = Stopwatch().start()
   ...
   >>> # do the first step of your program
   >>> timer.split()
   ... done in 0:00:00.201457
   >>> # do the second step of your program
   >>> timer.split()
   ... done in 0:00:00.100982

In the following guide, we assume that each line of code is executed immediately
after the previous one finished.
We use ``sleep()`` to simulate the running time of the program you want to evaluate.
We first initialize a stopwatch:

.. code-block:: python

   >>> from time import sleep
   >>> from bistiming import Stopwatch
   >>> timer = Stopwatch()
   >>> sleep(0.1)
   >>> timer.log_elapsed_time()  # 0:00:00
   Elapsed time: 0:00:00

The output of ``log_elapsed_time()`` is ``0:00:00`` because we haven't started the
stopwatch.
We will talk more about the initialization of ``Stopwatch`` in the following guide.
Now we start the stopwatch using ``start()``:

.. code-block:: python

   >>> timer.start()
   ...
   <bistiming.stopwatch.Stopwatch object at 0x7f800da5d1d0>
   >>> sleep(0.1)
   >>> timer.log_elapsed_time()  # 0:00:00.1
   Elapsed time: 0:00:00.100694
   >>> timer.get_elapsed_time()  # 0:00:00.1
   datetime.timedelta(microseconds=101825)

After 0.1s sleeping, we log the elapsed time.
The log is not exactly 0.1s because there are some overhead between the starting time
and logging time.
``get_elapsed_time()`` returns a ``datetime.timedelta`` object instead of printing.
Now we pause the timer using ``pause()`` after 0.1s more sleeping:

.. code-block:: python

   >>> sleep(0.1)
   >>> timer.pause()
   >>> timer.log_elapsed_time()  # 0:00:00.2
   Elapsed time: 0:00:00.201457
   >>> sleep(0.1)
   >>> timer.log_elapsed_time()  # 0:00:00.2
   Elapsed time: 0:00:00.201457

After pausing, the elapsed time remains exactly the same.
Now we introduce the splitting function, ``split()``, which saves the running time of the
current split and restarts the stopwatch:

.. code-block:: python

   >>> timer.split()  # 0:00:00.2
   ... done in 0:00:00.201457
   >>> timer.log_elapsed_time()  # 0:00:00
   Elapsed time: 0:00:00
   >>> timer.get_cumulative_elapsed_time()  # 0:00:00.2
   datetime.timedelta(microseconds=201457)

By default, ``start()`` and ``split()`` will output some logs.
They both have a ``verbose`` parameter to control whether to output.
If not set, they will use ``verbose_start`` and ``verbose_end`` defined during
initialization (``Stopwatch(verbose_start=True, verbose_end=True)``).
We can also use ``Stopwatch(verbose=False)`` to turn off all the output.

After splitting, the elapsed time is reset to 0.
There is also a convenient method ``get_cumulative_elapsed_time()`` that can return
the summation of all splits (including the currently running one).
Now we start the stopwatch again:

.. code-block:: python

   >>> sleep(0.1)
   >>> timer.start()
   ...
   <bistiming.stopwatch.Stopwatch object at 0x7f800da5d1d0>
   >>> sleep(0.1)
   >>> timer.log_elapsed_time()  # 0:00:00.1
   Elapsed time: 0:00:00.101419
   >>> timer.get_cumulative_elapsed_time()  # 0:00:00.3
   datetime.timedelta(microseconds=304080)

We can see that ``get_cumulative_elapsed_time()`` also increases. Let's try to split
more:

.. code-block:: python

   >>> timer.split()  # 0:00:00.1
   ... done in 0:00:00.103105
   >>> sleep(0.1)
   >>> timer.pause()
   >>> timer.split()  # 0:00:00.1
   ... done in 0:00:00.100982
   >>> timer.get_cumulative_elapsed_time()  # 0:00:00.4
   datetime.timedelta(microseconds=405544)
   >>> timer.splitted_elapsed_time  # [0:00:00.2, 0:00:00.1, 0:00:00.1]
   [datetime.timedelta(microseconds=201457),
    datetime.timedelta(microseconds=103105),
    datetime.timedelta(microseconds=100982)]

If we split without pausing, the stopwatch will keep running, so the second ``split()``
got 0.1s.
Currently, we have splitted 3 times.
We can use ``timer.splitted_elapsed_time`` to see the running time of the 3 splits.
The last thing we have not mentioned is ``reset()``:

.. code-block:: python

   >>> timer.reset()
   >>> timer.log_elapsed_time()  # 0:00:00
   Elapsed time: 0:00:00
   >>> timer.get_cumulative_elapsed_time()  # 0:00:00
   datetime.timedelta(0)
   >>> timer.splitted_elapsed_time  # []
   []
   >>> sleep(0.1)
   >>> timer.start()
   ...
   <bistiming.stopwatch.Stopwatch object at 0x7f800da5d1d0>
   >>> sleep(0.1)
   >>> timer.log_elapsed_time()  # 0:00:00.1
   Elapsed time: 0:00:00.101230

Documentation
-------------
See the `documentation <https://bistiming.readthedocs.io>`_ for more information.
