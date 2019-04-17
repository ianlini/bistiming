import pkg_resources

from .stopwatch import Stopwatch  # noqa: F401


SimpleTimer = Stopwatch  # backward-compatible to < 0.2


__version__ = pkg_resources.get_distribution("bistiming").version
