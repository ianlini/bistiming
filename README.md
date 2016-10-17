# bistiming
A timing and progress bar module for Python.

## Installation
- Install `bistiming`
  ```bash
  pip install bistiming
  ```

- If you want to use `IterTimer`:
  - For python < 3:

    ```
    pip install progressbar
    ```
  - For python >= 3:

    ```
    pip install progressbar33
    ```

## Testing
- For the current environment: `python setup test`.
- For python 2.7.12, 3.4.5, 3.5.2: `tox`.

## Examples
- This module provide two context managers for timing: `SimpleTimer` and `IterTimer`.

### SimpleTimer
- See [examples/simple_timing_example.py](examples/simple_timing_example.py) for the examples of `SimpleTimer`.
- The output of executing `python examples/simple_timing_example.py`:
  ```
  [Example 1]
  ...
  ... done in 0:00:01.001239

  [Example 2] timer with description
  ...Waiting
  ...Waiting done in 0:00:01.001262

  [Example 3] timer without starting message
  ...Waiting done in 0:00:01.001249

  [Example 4] timer without ending message
  ...Waiting

  [Example 5] rewrite the same line after ending
  ...Waiting done in 0:00:01.001291

  [Example 6] change the prefix
  [bistimer] Waiting
  [bistimer] Waiting done in 0:00:01.001201

  [Example 7] use python logging module
  [2016-10-17 22:49:47,121] INFO: __main__: ...Waiting
  [2016-10-17 22:49:48,123] INFO: __main__: ...Waiting done in 0:00:01.001263

  [Example 8] use python logging module with different log level
  [2016-10-17 22:49:48,123] DEBUG: __main__: ...Waiting
  [2016-10-17 22:49:49,125] DEBUG: __main__: ...Waiting done in 0:00:01.001245
  ```

### IterTimer
- See [examples/progressbar_timing_example.py](examples/progressbar_timing_example.py) for the examples of `IterTimer`.
