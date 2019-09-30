from __future__ import print_function, division, absolute_import, unicode_literals
from functools import partial
import logging
import datetime

import six


class Stopwatch(object):
    """A logging-friendly stopwatch with splitting function.

    Parameters
    ----------
    description : str
        The log to show at starting time (entering with-block or calling :meth:`start`)
        or ending time (exiting with-block or calling :meth:`split`).
    logger : :data:`~typing.Callable`
        A callable that accepts `logging_level` as its first argument and a :class:`str` to
        log as its first argument (basically, a :class:`logging.Logger` object). If `None`,
        use :func:`six.print_`, which is similar to the built-in :func:`print` in Python 3.
        When using with ``end_in_new_line=True``, it requires `end` and `flush` parameters.
    logging_level : int
        If `logger` is not `None`, this is the first argument to be passed to `logger`.
        Usually, this should be `logging.{DEBUG, INFO, WARNING, ERROR, CRITICAL}`.
        (default: `logging.INFO`)
    verbose_start : bool
        Wether to log at starting time (entering with-block or calling :meth:`start`).
    verbose_end : bool
        Wether to log at ending time (exiting with-block or calling :meth:`split`).
    end_in_new_line : bool
        Wether to log the ending log in a new line. If `False`, the starting log will
        not have a trailing new line, so the ending log can be logged in the same line.
        This requires `logger` to have `end` and `flush` parameters, or just
        ``logger=None``.
    prefix : str
        The prefix added to `description`.
    verbose : bool
        If `False`, turn off all the logs, that is, `verbose_start` and `verbose_end`
        will be set to `False`.

    Attributes
    ----------
    split_elapsed_time : List[datetime.timedelta]
        The elapsed time of each split (excluding the current split).
    """

    def __init__(self, description="", logger=None, logging_level=logging.INFO,
                 verbose_start=True, verbose_end=True, end_in_new_line=True,
                 prefix="...", verbose=True):
        if logger is not None:
            self.log = partial(logger.log, logging_level)
        else:
            self.log = six.print_
        self.description = prefix + description
        if verbose:
            self.verbose_start = verbose_start
            self.verbose_end = verbose_end
        else:
            self.verbose_start = False
            self.verbose_end = False
        self.end_in_new_line = end_in_new_line
        self.reset()

    def start(self, verbose=None, end_in_new_line=None):
        """Start the stopwatch if it is paused.

        If the stopwatch is already started, then nothing will happen.

        Parameters
        ----------
        verbose : Optional[bool]
            Wether to log. If `None`, use `verbose_start` set during initialization.
        end_in_new_line : Optional[bool]]
            If `False`, prevent logging the trailing new line. If `None`, use
            `end_in_new_line` set during initialization.
        """
        if self._start_time is not None and self._end_time is None:
            # the stopwatch is already running
            return self
        if verbose is None:
            verbose = self.verbose_start
        if verbose:
            if end_in_new_line is None:
                end_in_new_line = self.end_in_new_line
            if end_in_new_line:
                self.log(self.description)
            else:
                self.log(self.description, end="", flush=True)
        self._end_time = None
        self._start_time = datetime.datetime.now()
        return self

    def pause(self):
        """Pause the stopwatch.

        If the stopwatch is already paused, nothing will happen.
        """
        if self._end_time is not None:
            # the stopwatch is already paused
            return
        self._end_time = datetime.datetime.now()
        self._elapsed_time += self._end_time - self._start_time

    def get_elapsed_time(self):
        """Get the elapsed time of the current split.
        """
        if self._start_time is None or self._end_time is not None:
            # the stopwatch is paused
            return self._elapsed_time
        return self._elapsed_time + (datetime.datetime.now() - self._start_time)

    def get_cumulative_elapsed_time(self):
        """Get the cumulative elapsed time without considering splits.
        """
        return self._cumulative_elapsed_time + self.get_elapsed_time()

    def log_elapsed_time(self, prefix="Elapsed time: "):
        """Log the elapsed time of the current split.

        Parameters
        ----------
        prefix : str
            The prefix of the log.
        """
        self.log("{}{}".format(prefix, self.get_elapsed_time()))

    def split(self, verbose=None, end_in_new_line=None):
        """Save the elapsed time of the current split and restart the stopwatch.

        The current elapsed time will be appended to :attr:`split_elapsed_time`.
        If the stopwatch is paused, then it will remain paused.
        Otherwise, it will continue running.

        Parameters
        ----------
        verbose : Optional[bool]
            Wether to log. If `None`, use `verbose_end` set during initialization.
        end_in_new_line : Optional[bool]]
            Wether to log the `description`. If `None`, use `end_in_new_line` set during
            initialization.
        """
        elapsed_time = self.get_elapsed_time()
        self.split_elapsed_time.append(elapsed_time)
        self._cumulative_elapsed_time += elapsed_time
        self._elapsed_time = datetime.timedelta()
        if verbose is None:
            verbose = self.verbose_end
        if verbose:
            if end_in_new_line is None:
                end_in_new_line = self.end_in_new_line
            if end_in_new_line:
                self.log("{} done in {}".format(self.description, elapsed_time))
            else:
                self.log(" done in {}".format(elapsed_time))
        self._start_time = datetime.datetime.now()

    def reset(self):
        """Reset the stopwatch.
        """
        self._start_time = None
        self._end_time = None
        self._elapsed_time = datetime.timedelta()
        self._cumulative_elapsed_time = datetime.timedelta()
        self.split_elapsed_time = []

    def __enter__(self):
        """Call :meth:`start`.
        """
        return self.start()

    def __exit__(self, exc_type, exc, exc_tb):
        """Call :meth:`pause` and then :meth:`split`.
        """
        self.pause()
        self.split()
