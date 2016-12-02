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
        self.start_time = None
        self.end_time = None
        self.elapsed_time = None

    def __enter__(self):
        if self.verbose_start:
            if self.end_in_new_line:
                self.log(self.description)
            else:
                self.log(self.description, end="", flush=True)

        self.start_time = datetime.datetime.now()
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        self.end_time = datetime.datetime.now()
        self.elapsed_time = self.end_time - self.start_time
        if self.verbose_end:
            if self.end_in_new_line:
                msg = self.description
            else:
                msg = ""
            msg += " done in {}".format(self.elapsed_time)
            self.log(msg)

