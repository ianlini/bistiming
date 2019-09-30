from __future__ import print_function, division, absolute_import, unicode_literals
import datetime


def div_timedelta_int(d, i):
    d_us = d.microseconds + 1000000 * (d.seconds + 86400 * d.days)
    return datetime.timedelta(microseconds=d_us / i)


def div_timedelta(d1, d2):
    if isinstance(d2, int):
        return div_timedelta_int(d1, d2)
    d1_us = d1.microseconds + 1000000 * (d1.seconds + 86400 * d1.days)
    d2_us = d2.microseconds + 1000000 * (d2.seconds + 86400 * d2.days)
    return d1_us / d2_us
