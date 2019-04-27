__all__ = ['Stopwatch', 'MultiStopwatch']

import pkg_resources
__version__ = pkg_resources.get_distribution("bistiming").version

from .stopwatch import Stopwatch  # noqa: F401
from .multistopwatch import MultiStopwatch  # noqa: F401


SimpleTimer = Stopwatch  # backward-compatible to < 0.2
