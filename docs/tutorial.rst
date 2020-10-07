Tutorial
========
In the following tutorial, we assume that each line of code is executed immediately
after the previous one finished.
We use :func:`~time.sleep` to simulate the running time of the program we want to evaluate.

Context Manager
+++++++++++++++

The simplest way to use BisTiming is using the context manager :class:`~bistiming.Stopwatch`
to include the code we want to evaluate:

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
parameter in :meth:`~bistiming.Stopwatch`:

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
`verbose_start`:

>>> with Stopwatch("Waiting", verbose_start=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
do something
finished something
...Waiting done in 0:00:00.100333

Similarly, if we don't want to output anything when exiting the block, we can use the
parameter `verbose_end`:

>>> with Stopwatch("Waiting", verbose_end=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
...Waiting
do something
finished something

If don't want any output, we can use the parameter `verbose` to turn off all of them:

>>> with Stopwatch(verbose=False):
...     print("do something")
...     sleep(0.1)
...     print("finished something")
...
do something
finished something

Sometimes we only want to see one line for both entering and exiting.
We can use the parameter `end_in_new_line`:

>>> with Stopwatch("Waiting", end_in_new_line=False):
...     sleep(0.1)
...
...Waiting done in 0:00:00.100340

This will output ``...Waiting`` first, and when exiting the block, ``done in...``
will be appended after that line.

If you don't like the default prefix ``...``, you can use the parameter `prefix` to
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

The built-in module :mod:`logging` is very useful when we are developing a complicated
service.
We can use the parameter `logger` to tell the stopwatch to output using a logger:

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

We can also configure the logging level using the parameter `logging_level`:

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

Each item in :attr:`~bistiming.Stopwatch.split_elapsed_time` is the running time of
the code segment in each iteration, and we can use
:meth:`~bistiming.Stopwatch.get_cumulative_elapsed_time`
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

When using the low-level API, we first initialize a stopwatch (we have talked a lot
about the initialization in the `context manager <#context-manager>`_ section):

>>> from time import sleep
>>> from bistiming import Stopwatch
>>> timer = Stopwatch("Waiting")
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00
Elapsed time: 0:00:00

The output of :meth:`~bistiming.Stopwatch.log_elapsed_time` is ``0:00:00``
because we haven't started the stopwatch.

Now we start the stopwatch using :meth:`~bistiming.Stopwatch.start`:

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
:meth:`~bistiming.Stopwatch.get_elapsed_time` returns a :class:`datetime.timedelta`
object instead of printing.

Now we pause the timer using :meth:`~bistiming.Stopwatch.pause()` after 0.1s more sleeping:

>>> sleep(0.1)
>>> timer.pause()
>>> timer.log_elapsed_time()  # 0:00:00.2
Elapsed time: 0:00:00.202967
>>> sleep(0.1)
>>> timer.log_elapsed_time()  # 0:00:00.2
Elapsed time: 0:00:00.202967

After pausing, the elapsed time remains exactly the same.

Now we introduce the splitting function, :meth:`~bistiming.Stopwatch.split`,
which stores the running time of the current split and restarts the stopwatch:

>>> timer.split()  # 0:00:00.2
...Waiting done in 0:00:00.202967
>>> timer.log_elapsed_time()  # 0:00:00
Elapsed time: 0:00:00
>>> timer.get_cumulative_elapsed_time()  # 0:00:00.2
datetime.timedelta(microseconds=202967)

By default, :meth:`~bistiming.Stopwatch.start` and :meth:`~bistiming.Stopwatch.split`
will output some logs.
They both have a `verbose` parameter to control whether to output.
If not set, they will use `verbose_start` and `verbose_end` defined during
initialization (``Stopwatch(verbose_start=True, verbose_end=True)``).
We can also use ``Stopwatch(verbose=False)`` to turn off all the output.

After splitting, the elapsed time is reset to 0.
There is also a convenient method :meth:`~bistiming.Stopwatch.get_cumulative_elapsed_time`
that can return the total running time of all splits (including the currently running one).
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

We can see that :meth:`~bistiming.Stopwatch.get_cumulative_elapsed_time` also increases.

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

If we split without pausing, the stopwatch will keep running, so the second
:meth:`~bistiming.Stopwatch.split` got 0.1s.
Currently, we have split 3 times.
We can use :attr:`~bistiming.Stopwatch.split_elapsed_time` to see the running
time of the 3 splits.

The last thing we have not mentioned is :meth:`~bistiming.Stopwatch.reset`:

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

:meth:`~bistiming.Stopwatch.reset` will clear all the states in the stopwatch
just like a whole new stopwatch.

Advance Profiling
+++++++++++++++++
There is another useful tool `line_profiler <https://github.com/rkern/line_profiler>`_
for line-by-line performance profiling.
It's very convenient because we only need to add one line to our code to enable the profiling,
and the result is an easy-to-understand statistics.
However, it has a large overhead when some lines are very simple and can be finished in
few nanoseconds.
The running time of those lines will be overestimated especially when they are hit much
more times than other lines.

:class:`~bistiming.MultiStopwatch` in this package contains multiple
:class:`~bistiming.Stopwatch`, so we can use them to define each code segment
we want to evaluate and compare easily:

>>> from time import sleep
>>> from bistiming import MultiStopwatch
>>> timers = MultiStopwatch(2, verbose=False)
>>> for i in range(5):
...     for i in range(2):
...         with timers[0]:
...             sleep(0.1)
...     with timers[1]:
...         sleep(0.1)
...
>>> timers.get_cumulative_elapsed_time()
[datetime.timedelta(seconds=1, microseconds=2417), datetime.timedelta(microseconds=501861)]
>>> timers.get_n_splits()
[10, 5]
>>> timers.get_mean_per_split()
[datetime.timedelta(microseconds=100242), datetime.timedelta(microseconds=100372)]
>>> timers.get_percentage()
[0.6663774913945427, 0.3336225086054572]
>>> timers.get_statistics()
{'cumulative_elapsed_time': [datetime.timedelta(seconds=1, microseconds=2417),
                             datetime.timedelta(microseconds=501861)],
 'mean_per_split': [datetime.timedelta(microseconds=100242),
                    datetime.timedelta(microseconds=100372)],
 'n_splits': [10, 5],
 'percentage': [0.6663774913945427, 0.3336225086054572]}
>>> print(timers.format_statistics())
╒═══════════════════════════╤══════════════╤════════════╤══════════════════╕
│ cumulative_elapsed_time   │   percentage │   n_splits │ mean_per_split   │
╞═══════════════════════════╪══════════════╪════════════╪══════════════════╡
│ 0:00:01.002417            │     0.666377 │         10 │ 0:00:00.100242   │
├───────────────────────────┼──────────────┼────────────┼──────────────────┤
│ 0:00:00.501861            │     0.333623 │          5 │ 0:00:00.100372   │
╘═══════════════════════════╧══════════════╧════════════╧══════════════════╛

If we actually don't care about the inner loop, we can move the ``timer[0]`` outside
to reduce the overhead:

>>> timers = MultiStopwatch(2, verbose=False)
>>> for i in range(5):
...     with timers[0]:
...         for i in range(2):
...             sleep(0.1)
...     with timers[1]:
...         sleep(0.1)
...
>>> print(timers.format_statistics())
╒═══════════════════════════╤══════════════╤════════════╤══════════════════╕
│ cumulative_elapsed_time   │   percentage │   n_splits │ mean_per_split   │
╞═══════════════════════════╪══════════════╪════════════╪══════════════════╡
│ 0:00:01.003944            │      0.66679 │          5 │ 0:00:00.200789   │
├───────────────────────────┼──────────────┼────────────┼──────────────────┤
│ 0:00:00.501694            │      0.33321 │          5 │ 0:00:00.100339   │
╘═══════════════════════════╧══════════════╧════════════╧══════════════════╛

Like we said previously, if the inner loop is very fast, and we run it much more times
than other lines, its running time will be overestimated:

>>> timers1 = MultiStopwatch(2, verbose=False)
>>> for i in range(5):
...     for i in range(100000):
...         with timers1[0]:
...             a = 0
...     with timers1[1]:
...         sleep(0.1)
...
>>> timers2 = MultiStopwatch(2, verbose=False)
>>> for i in range(5):
...     with timers2[0]:
...         for i in range(100000):
...             a = 0
...     with timers2[1]:
...         sleep(0.1)
...
>>> print(timers1.format_statistics())
╒═══════════════════════════╤══════════════╤════════════╤══════════════════╕
│ cumulative_elapsed_time   │   percentage │   n_splits │ mean_per_split   │
╞═══════════════════════════╪══════════════╪════════════╪══════════════════╡
│ 0:00:00.558187            │     0.526846 │     500000 │ 0:00:00.000001   │
├───────────────────────────┼──────────────┼────────────┼──────────────────┤
│ 0:00:00.501300            │     0.473154 │          5 │ 0:00:00.100260   │
╘═══════════════════════════╧══════════════╧════════════╧══════════════════╛
>>> print(timers2.format_statistics())
╒═══════════════════════════╤══════════════╤════════════╤══════════════════╕
│ cumulative_elapsed_time   │   percentage │   n_splits │ mean_per_split   │
╞═══════════════════════════╪══════════════╪════════════╪══════════════════╡
│ 0:00:00.068416            │     0.120047 │          5 │ 0:00:00.013683   │
├───────────────────────────┼──────────────┼────────────┼──────────────────┤
│ 0:00:00.501496            │     0.879953 │          5 │ 0:00:00.100299   │
╘═══════════════════════════╧══════════════╧════════════╧══════════════════╛

We can notice a big difference between ``timers1`` and ``timers2``.
``timers2`` is more reasonable if we are finding the bottleneck of the code
because ``sleep(0.1)`` actually takes much more time than 100000 times of ``a = 0``.
