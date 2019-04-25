from __future__ import print_function, division, absolute_import, unicode_literals
from six.moves import zip


def assert_timedelta_close_seconds_list(d_list, s_list, epsilon=0.05):
    for d, s in zip(d_list, s_list):
        assert_timedelta_close_seconds(d, s, epsilon)


def assert_timedelta_close_seconds(d, s, epsilon=0.05):
    d_s = d.days * 86400 + d.seconds + d.microseconds * 0.000001
    percentage_error = abs(d_s - s) / s
    assert percentage_error < epsilon
