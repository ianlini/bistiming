__all__ = ["Stopwatch", "MultiStopwatch"]

try:
    # for Python >= 3.8
    from importlib.metadata import version
except ImportError:
    # for Python < 3.8, the package importlib-metadata will be installed
    from importlib_metadata import version

__version__ = version("bistiming")

from .stopwatch import Stopwatch  # noqa: F401
from .multistopwatch import MultiStopwatch  # noqa: F401

SimpleTimer = Stopwatch  # backward-compatible to < 0.2
