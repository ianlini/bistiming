# BisTiming

[![](https://img.shields.io/travis/ianlini/bistiming/master.svg)](https://travis-ci.org/ianlini/bistiming)
[![](https://img.shields.io/pypi/v/bistiming.svg)](https://pypi.org/project/bistiming/)
[![](https://img.shields.io/pypi/l/bistiming.svg)](https://pypi.org/project/bistiming/)

A logging-friendly timing module for Python.

## Installation

```bash
pip install bistiming
```

## Testing

* Linter: `flake8`.
* For the current environment: `python setup.py test`.
* For Python 2.7, 3.5, 3.6, 3.7, flake8 and installation test: `tox`.

### Examples

* See [examples/stopwatch_examples.py](examples/stopwatch_examples.py) for the examples of `Stopwatch`.
* The output of executing `python examples/stopwatch_examples.py`:
  ![The output of executing python examples/stopwatch_examples.py](examples/simple_timing_example.gif)
