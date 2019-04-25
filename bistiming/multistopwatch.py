from collections import UserList
import datetime

from . import Stopwatch


class MultiStopwatch(UserList):
    def __init__(self, iterable, *args, **kwargs):
        if isinstance(iterable, int):
            n = iterable
            super(MultiStopwatch, self).__init__(Stopwatch(*args, **kwargs) for i in range(n))
        else:
            assert not args and not kwargs
            super(MultiStopwatch, self).__init__(iterable)

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
        return [t / sum_elapsed_time for t in cumulative_elapsed_time]

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
        return [(sum(stopwatch.split_elapsed_time, datetime.timedelta())
                 / len(stopwatch.split_elapsed_time))
                for stopwatch in self]
