from __future__ import print_function, division, absolute_import, unicode_literals
from time import sleep
import unittest

from six.moves import range, zip
from examples import multistopwatch_examples
from bistiming import MultiStopwatch

from .utils import assert_timedelta_close_seconds_list, isclose


class TestMultiStopwatch(unittest.TestCase):
    def test_multistopwatch_examples(self):
        multistopwatch_examples.main()

    def test_muulti_stopwatch(self):
        timers = MultiStopwatch(2, verbose=False)
        for i in range(5):
            for i in range(2):
                with timers[0]:
                    sleep(0.1)
            with timers[1]:
                sleep(0.1)

        # test get_cumulative_elapsed_time()
        assert_timedelta_close_seconds_list(
            timers.get_cumulative_elapsed_time(),
            [1, 0.5])

        # test get_percentage()
        for p, exp in zip(timers.get_percentage(), [2 / 3, 1 / 3]):
            self.assertTrue(isclose(p, exp, rel_tol=0.05))

        # test get_n_splits()
        self.assertListEqual(timers.get_n_splits(), [10, 5])

        # test get_mean_per_split()
        assert_timedelta_close_seconds_list(
            timers.get_mean_per_split(),
            [0.1, 0.1])

        # test get_statistics()
        self.assertListEqual(
            sorted(timers.get_statistics().keys()),
            ['cumulative_elapsed_time', 'mean_per_split', 'n_splits', 'percentage'])
