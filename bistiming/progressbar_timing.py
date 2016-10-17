import datetime
from progressbar import (ProgressBar, Percentage, UnknownLength,
                         Bar, SimpleProgress, Timer, ETA)


class PreciseTimer(Timer):
    """Widget which displays the elapsed seconds."""

    @staticmethod
    def format_time(seconds):
        """Formats time as the string "HH:MM:SS"."""
        return str(datetime.timedelta(seconds=seconds))


class PreciseETA(ETA):
    """Widget which attempts to estimate the time of arrival."""

    def update(self, pbar):
        """Updates the widget to show the ETA or total time when finished."""

        if pbar.currval == 0:
            return 'ETA:  --:--:--'
        elif pbar.finished:
            return 'Time: %s' % PreciseTimer.format_time(pbar.seconds_elapsed)
        else:
            elapsed = pbar.seconds_elapsed
            eta = elapsed * pbar.maxval / pbar.currval - elapsed
            return 'ETA:  %s' % PreciseTimer.format_time(eta)


class IterTimer(object):

    def __init__(self, name="", total=UnknownLength, period=1, verbose=3):
        """
        Args:
            verbose: 0: no output, do nothing
                     1: only output in start
                     2: only output in start and end
                     3: output in progresss
        """
        self.verbose = verbose
        self.period = period
        if verbose >= 2:
            widgets = ["...", name]
            if total is not UnknownLength:
                widgets.extend([" ", Bar(), " ", SimpleProgress("/"),
                                " (", Percentage(), ")  ", PreciseETA()])
            else:
                widgets.extend([" (", PreciseTimer(), ")"])
            self.pbar = ProgressBar(widgets=widgets, maxval=total)
        elif verbose >= 1:
            print("..." + name)

    def __enter__(self):
        if self.verbose >= 2:
            self.pbar.start()
            if self.verbose == 2:
                print("")
        return self

    def __exit__(self, exc_type, exc, exc_tb):
        if self.verbose >= 2:
            self.pbar.widgets.insert(2, " done")
            self.pbar.finish()

    def update(self, i, total=None):
        if i % self.period == 0:
            if self.verbose >= 2 and total is not None:
                self.pbar.maxval = total
            if self.verbose >= 3:
                self.pbar.update(i)
