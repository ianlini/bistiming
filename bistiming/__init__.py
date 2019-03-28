import pkg_resources

from .simple_timing import SimpleTimer  # noqa: F401


__all__ = ['progressbar_timing', 'simple_timing']
__version__ = pkg_resources.get_distribution("bistiming").version
