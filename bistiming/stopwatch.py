from functools import partial
import logging
import datetime

import six


class Stopwatch(object):

    def __init__(self, description="", logger=None, logging_level=logging.INFO,
                 verbose_start=True, verbose_end=True, end_in_new_line=True,
                 prefix="..."):
        """A logging-friendly stopwatch with splitting function.

        Parameters
        ----------
        description : str
            The message to show at starting time (entering with-block or calling ``start()``)
            or ending time (exiting with-block or calling ``split()``). (default: ``""``)
        logger : Callable
            A ``Callable`` that accepts ``logging_level`` as its first argument and a ``str`` to
            log as its first argument (basically, a ``logging.Logger`` object). If ``None``, use
            ``six.print_``, which is similar to the built-in ``print`` in Python 3. When using with
            ``end_in_new_line=True``, it requires ``end`` and ``flush`` parameters.
            (default: ``None``)
        logging_level : int
            If ``logger`` is not ``None``, this is the first argument to be passed to ``logger``.
            Usually, this should be ``logging.{DEBUG, INFO, WARNING, ERROR, CRITICAL}``.
            (default: ``logging.INFO``)
        verbose_start : bool
            Wether to log at starting time (entering with-block or calling ``start()``).
            (default: ``True``)
        verbose_end : bool
            Wether to log at ending time (exiting with-block or calling ``split()``).
            (default: ``True``)
        end_in_new_line : bool
            Wether to log the ending message in a new line. If ``False``, the starting message will
            not have a trailing new line, so the ending message can be logged in the same line.
            (default: ``True``)
        prefix : str
            The prefix added to ``description``.
        """
        if logger is not None:
            self.log = partial(logger.log, logging_level)
        else:
            self.log = six.print_
        self.description = prefix + description
        self.verbose_start = verbose_start
        self.verbose_end = verbose_end
        self.end_in_new_line = end_in_new_line
        self._start_time = None
        self._end_time = None
        self._elapsed_time = datetime.timedelta()
        self.cumulative_elapsed_time = datetime.timedelta()
        self.splitted_elapsed_time = []

    def start(self, verbose=None, end_in_new_line=None):
        if self._start_time is not None and self._end_time is None:
            # the timer is already running
            return
        if verbose is None:
            verbose = self.verbose_start
        if end_in_new_line is None:
            end_in_new_line = self.end_in_new_line
        if verbose:
            if end_in_new_line:
                self.log(self.description)
            else:
                self.log(self.description, end="", flush=True)
        self._end_time = None
        self._start_time = datetime.datetime.now()
        return self

    def pause(self):
        if self._end_time is not None:
            # the timer is already paused
            return
        self._end_time = datetime.datetime.now()
        self._elapsed_time += self._end_time - self._start_time

    def get_elapsed_time(self):
        if self._start_time is None or self._end_time is not None:
            # the timer is already paused
            return self._elapsed_time
        return self._elapsed_time + (datetime.datetime.now() - self._start_time)

    def log_elapsed_time(self, prefix="Elapsed time: "):
        self.log("{}{}".format(prefix, self.get_elapsed_time()))

    def split(self, verbose=None, end_in_new_line=None):
        elapsed_time = self.get_elapsed_time()
        self.splitted_elapsed_time.append(elapsed_time)
        self.cumulative_elapsed_time += elapsed_time
        self._start_time += elapsed_time
        self._elapsed_time = datetime.timedelta()
        if verbose is None:
            verbose = self.verbose_end
        if end_in_new_line is None:
            end_in_new_line = self.end_in_new_line
        if verbose:
            if end_in_new_line:
                self.log("{} done in {}".format(self.description, elapsed_time))
            else:
                self.log(" done in {}".format(elapsed_time))

    def reset(self):
        pass

    def __enter__(self):
        return self.start()

    def __exit__(self, exc_type, exc, exc_tb):
        self.pause()
        self.split()
