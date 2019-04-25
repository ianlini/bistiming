from collections import UserList

from . import Stopwatch


class MultiStopwatch(UserList):
    def __init__(self, iterable, *args, **kwargs):
        if isinstance(iterable, int):
            n = iterable
            super(MultiStopwatch, self).__init__(Stopwatch(*args, **kwargs) for i in range(n))
        else:
            assert not args and not kwargs
            super(MultiStopwatch, self).__init__(iterable)
