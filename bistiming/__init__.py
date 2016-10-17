from .simple_timing import SimpleTimer
try:
    from .progressbar_timing import IterTimer
except ImportError as exc:
    import sys
    if ((sys.version_info[0] < 3 and str(exc) == "No module named progressbar")
            or exc.name == 'progressbar'):
        def IterTimer(*args, **kwarg):  # pylint: disable=unused-argument
            raise ImportError("please install progressbar module using "
                              "\"pip install progressbar\" in python 2 or "
                              "\"pip install progressbar33\" in python 3")
    else:
        raise


__all__ = ['progressbar_timing', 'simple_timing']
__version__ = "0.1.0"
