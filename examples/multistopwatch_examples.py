from time import sleep

from bistiming import MultiStopwatch


def basic_example():
    timers = MultiStopwatch(2, verbose=False)
    for i in range(5):
        with timers[0]:
            sleep(0.1)
        with timers[1]:
            sleep(0.2)
    print("timers[0]:", timers[0].get_cumulative_elapsed_time())
    print("timers[1]:", timers[1].get_cumulative_elapsed_time())


def main():
    basic_example()


if __name__ == '__main__':
    main()
