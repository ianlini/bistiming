from time import sleep

from bistiming import MultiStopwatch


def basic_example():
    timers = MultiStopwatch(2, verbose=False)
    for i in range(5):
        for i in range(2):
            with timers[0]:
                sleep(0.1)
        with timers[1]:
            sleep(0.1)
    print("get_cumulative_elapsed_time():", timers.get_cumulative_elapsed_time())
    print("get_n_splits():", timers.get_n_splits())
    print("get_mean_per_split():", timers.get_mean_per_split())
    print("get_percentage():", timers.get_percentage())


def main():
    basic_example()


if __name__ == '__main__':
    main()
