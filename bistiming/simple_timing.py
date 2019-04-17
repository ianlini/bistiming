from functools import partial
import logging
import datetime

import six


class SimpleTimer(object):

    def __init__(self, description="", logger=None, logging_level=logging.INFO,
                 verbose_start=True, verbose_end=True, end_in_new_line=True,
                 prefix="..."):
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
