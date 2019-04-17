from time import sleep
import logging

from bistiming import Stopwatch


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def no_arg_example():
    print("[no_arg_example]")
    with Stopwatch():
        sleep(1)


def description_example():
    print("[description_example] stopwatch with description")
    with Stopwatch("Waiting"):
        sleep(1)


def hide_starting_message_example():
    print("[hide_starting_message_example] hide starting message")
    with Stopwatch("Waiting", verbose_start=False):
        sleep(1)


def hide_ending_message_example():
    print("[hide_ending_message_example] hide ending message")
    with Stopwatch("Waiting", verbose_end=False):
        sleep(1)


def same_line_message_example():
    print("[same_line_message_example] write the ending message at the same line")
    with Stopwatch("Waiting", end_in_new_line=False):
        sleep(1)


def changing_prefix_example():
    print("[changing_prefix_example] change the prefix")
    with Stopwatch("Waiting", prefix="[bistiming] "):
        sleep(1)


def logging_example():
    print("[logging_example] use python logging module")
    with Stopwatch("Waiting", logger=logger):
        sleep(1)


def logging_level_example():
    print("[logging_level_example] use python logging module with different log level")
    with Stopwatch("Waiting", logger=logger, logging_level=logging.DEBUG):
        sleep(1)


def cumulative_elapsed_time_example():
    print("[cumulative_elapsed_time_example] use python logging module with different log level")
    timer = Stopwatch("Waiting")
    with timer:
        sleep(1)
    sleep(1)
    with timer:
        sleep(1)
        timer.log_elapsed_time(prefix="timer.log_elapsed_time(): ")  # 0:00:01....
        print("timer.get_elapsed_time():", timer.get_elapsed_time())  # 0:00:01....
    print("timer.splitted_elapsed_time:", timer.splitted_elapsed_time)
    # [datetime.timedelta(seconds=1), datetime.timedelta(seconds=1)]
    print("timer.cumulative_elapsed_time:", timer.cumulative_elapsed_time)  # 0:00:02....


def main():
    no_arg_example()
    print()
    description_example()
    print()
    hide_starting_message_example()
    print()
    hide_ending_message_example()
    print()
    same_line_message_example()
    print()
    changing_prefix_example()
    print()
    logging_example()
    print()
    logging_level_example()
    print()
    cumulative_elapsed_time_example()


if __name__ == '__main__':
    main()
