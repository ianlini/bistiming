from __future__ import print_function, division, absolute_import, unicode_literals

from time import sleep
import pprint

from six.moves import range

from bistiming import MultiStopwatch


def basic_example():
    timers = MultiStopwatch(2, verbose=False)
    for _ in range(5):
        for _ in range(2):
            with timers[0]:
                sleep(0.1)
        with timers[1]:
            sleep(0.1)
    print("get_cumulative_elapsed_time():", timers.get_cumulative_elapsed_time())
    print("get_n_splits():", timers.get_n_splits())
    print("get_mean_per_split():", timers.get_mean_per_split())
    print("get_percentage():", timers.get_percentage())
    print("get_statistics():")
    pprint.pprint(timers.get_statistics())
    print(timers.format_statistics())


def main():
    basic_example()


if __name__ == "__main__":
    main()
