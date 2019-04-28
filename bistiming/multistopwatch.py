from __future__ import print_function, division, absolute_import, unicode_literals
import datetime

from six.moves import UserList, range

from . import Stopwatch
from .utils import div_timedelta


class MultiStopwatch(UserList):
    """Use multiple :class:`Stopwatch` to profile and compare multiple code segments.

    Because this class is inheritted from :class:`~collections.UserList`,
    it also supports all the methods in the built-in :class:`list`.

    Parameters
    ----------
    n : Union[int, Iterable, None]
        If `n` is an `int`, then initialize a `list` with `n` :class:`Stopwatch`.
        If `n` is `None`, then initialize an empty `list`.
        Otherwise, directly use `n` to initialize a `list`.
    *args
        Other arguments will be passed to initialize :class:`Stopwatch`.
    **kwargs
        Other keyword arguments will be passed to initialize :class:`Stopwatch`.
    """
    def __init__(self, n=None, *args, **kwargs):
        if isinstance(n, int):
            super(MultiStopwatch, self).__init__(Stopwatch(*args, **kwargs) for i in range(n))
        else:
            super(MultiStopwatch, self).__init__(n)

    def get_cumulative_elapsed_time(self):
        """Get the cumulative elapsed time of each stopwatch (including the current split).

        Returns
        -------
        cumulative_elapsed_time : List[datetime.timedelta]
        """
        return [stopwatch.get_cumulative_elapsed_time() for stopwatch in self]

    def get_percentage(self):
        """Get the cumulative time percentage of each stopwatch (including the current split).

        Returns
        -------
        cumulative_elapsed_time_percentage : List[float]
        """
        cumulative_elapsed_time = self.get_cumulative_elapsed_time()
        sum_elapsed_time = sum(cumulative_elapsed_time, datetime.timedelta())
        if not sum_elapsed_time:
            raise ValueError("cannot get percentage if there is no any elapsed time")
        return [div_timedelta(t, sum_elapsed_time) for t in cumulative_elapsed_time]

    def get_n_splits(self):
        """Get number of splits of each stopwatch (excluding the current split).

        Returns
        -------
        n_splits : List[int]
        """
        return [len(stopwatch.split_elapsed_time) for stopwatch in self]

    def get_mean_per_split(self):
        """Get the mean elapsed time per split of each stopwatch (excluding the current split).

        Returns
        -------
        mean_elapsed_time_per_split : List[datetime.timedelta]
        """
        return [div_timedelta(sum(stopwatch.split_elapsed_time, datetime.timedelta()),
                              len(stopwatch.split_elapsed_time))
                if stopwatch.split_elapsed_time else datetime.timedelta()
                for stopwatch in self]

    def get_statistics(self):
        """Get all statistics as a dictionary.

        Returns
        -------
        statistics : Dict[str, List]
        """
        return {
            'cumulative_elapsed_time': self.get_cumulative_elapsed_time(),
            'percentage': self.get_percentage(),
            'n_splits': self.get_n_splits(),
            'mean_per_split': self.get_mean_per_split(),
        }
