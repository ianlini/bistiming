# BisTiming

[![](https://img.shields.io/travis/ianlini/bistiming/master.svg)](https://travis-ci.org/ianlini/bistiming)
[![](https://img.shields.io/pypi/v/bistiming.svg)](https://pypi.org/project/bistiming/)
[![](https://img.shields.io/pypi/l/bistiming.svg)](https://pypi.org/project/bistiming/)

A timing and progress bar module for Python.

## Installation

* Install `bistiming`

  ```bash
  pip install bistiming
  ```

* If you want to use `IterTimer`:
  * For Python < 3:

    ```bash
    pip install progressbar
    ```

  * For Python >= 3:

    ```bash
    pip install progressbar33
    ```

## Testing

* For the current environment: `python setup test`.
* For Python 2.7.12, 3.4.5, 3.5.2 and installation test: `tox`.

## Examples

* This module provide two context managers for timing: `SimpleTimer` and `IterTimer`.

### SimpleTimer

* See [examples/simple_timing_example.py](examples/simple_timing_example.py) for the examples of `SimpleTimer`.
* The output of executing `python examples/simple_timing_example.py`:
  ![The output of executing python examples/simple_timing_example.py](examples/simple_timing_example.gif)

### IterTimer

* See [examples/progressbar_timing_example.py](examples/progressbar_timing_example.py) for the examples of `IterTimer`.
* The output of executing `python examples/progressbar_timing_example.py`:
  ![The output of executing python examples/progressbar_timing_example.py](examples/progressbar_timing_example.gif)
