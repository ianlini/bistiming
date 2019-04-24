import datetime
from time import sleep

from examples import stopwatch_examples
from bistiming import Stopwatch


def test_stopwatch_examples():
    stopwatch_examples.main()


def assert_timedelta_close_seconds(d, s, epsilon=0.05):
    d_s = d.days * 86400 + d.seconds + d.microseconds * 0.000001
    percentage_error = abs(d_s - s) / s
    assert percentage_error < epsilon


def test_low_level_api():
    timer = Stopwatch()
    sleep(0.1)
    assert timer.get_elapsed_time() == datetime.timedelta()
    timer.start()
    sleep(0.1)
    assert_timedelta_close_seconds(timer.get_elapsed_time(), 0.1)
    sleep(0.1)
    timer.pause()
    assert_timedelta_close_seconds(timer.get_elapsed_time(), 0.2)
    sleep(0.1)
    assert_timedelta_close_seconds(timer.get_elapsed_time(), 0.2)
    timer.split()  # 0:00:00.2
    assert timer.get_elapsed_time() == datetime.timedelta()
    assert_timedelta_close_seconds(timer.get_cumulative_elapsed_time(), 0.2)
    sleep(0.1)
    timer.start()
    sleep(0.1)
    assert_timedelta_close_seconds(timer.get_elapsed_time(), 0.1)
    assert_timedelta_close_seconds(timer.get_cumulative_elapsed_time(), 0.3)
    timer.split()  # 0:00:00.1
    sleep(0.1)
    timer.pause()
    timer.split()  # 0:00:00.1
    assert_timedelta_close_seconds(timer.get_cumulative_elapsed_time(), 0.4)
    assert_timedelta_close_seconds(timer.split_elapsed_time[0], 0.2)
    assert_timedelta_close_seconds(timer.split_elapsed_time[1], 0.1)
    assert_timedelta_close_seconds(timer.split_elapsed_time[2], 0.1)
    timer.reset()

    assert timer.get_elapsed_time() == datetime.timedelta()
    assert timer.get_cumulative_elapsed_time() == datetime.timedelta()
    assert timer.split_elapsed_time == []
    sleep(0.1)
    timer.start()
    sleep(0.1)
    assert_timedelta_close_seconds(timer.get_elapsed_time(), 0.1)
