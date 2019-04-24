from time import sleep
import logging

from bistiming import Stopwatch


logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
logger = logging.getLogger(__name__)


def basic_example():
    print("[basic_example]")
    timer = Stopwatch()
    sleep(0.1)
    timer.log_elapsed_time()  # 0:00:00
    timer.start()
    sleep(0.1)
    timer.log_elapsed_time()  # 0:00:00.1
    sleep(0.1)
    timer.pause()
    timer.log_elapsed_time()  # 0:00:00.2
    sleep(0.1)
    timer.log_elapsed_time()  # 0:00:00.2
    timer.split()  # 0:00:00.2
    timer.log_elapsed_time()  # 0:00:00
    print("timer.get_cumulative_elapsed_time():", timer.get_cumulative_elapsed_time())  # 0:00:00.2
    sleep(0.1)
    timer.start()
    sleep(0.1)
    timer.log_elapsed_time()  # 0:00:00.1
    print("timer.get_cumulative_elapsed_time():", timer.get_cumulative_elapsed_time())  # 0:00:00.3
    timer.split()  # 0:00:00.1
    sleep(0.1)
    timer.pause()
    timer.split()  # 0:00:00.1
    print("timer.get_cumulative_elapsed_time():", timer.get_cumulative_elapsed_time())  # 0:00:00.4
    print("timer.split_elapsed_time:", [str(delta) for delta in timer.split_elapsed_time])
    # [0:00:00.2, 0:00:00.1, 0:00:00.1]
    timer.reset()

    timer.log_elapsed_time()  # 0:00:00
    print("timer.get_cumulative_elapsed_time():", timer.get_cumulative_elapsed_time())  # 0:00:00
    print("timer.split_elapsed_time:", timer.split_elapsed_time)  # []
    sleep(0.1)
    timer.start()
    sleep(0.1)
    timer.log_elapsed_time()  # 0:00:00.1


def basic_context_manager_example():
    print("[basic_context_manager_example]")
    with Stopwatch():
        sleep(1)


def description_example():
    print("[description_example] stopwatch with description")
    with Stopwatch("Waiting"):
        sleep(1)


def hide_starting_log_example():
    print("[hide_starting_log_example] hide starting log")
    with Stopwatch("Waiting", verbose_start=False):
        sleep(1)


def hide_ending_log_example():
    print("[hide_ending_log_example] hide ending log")
    with Stopwatch("Waiting", verbose_end=False):
        sleep(1)


def hide_all_logs_example():
    print("[hide_all_logs_example] hide all logs")
    with Stopwatch(verbose=False):
        sleep(1)


def same_line_log_example():
    print("[same_line_log_example] write the ending log at the same line")
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
    print("timer.split_elapsed_time:", timer.split_elapsed_time)
    # [datetime.timedelta(seconds=1), datetime.timedelta(seconds=1)]
    print("timer.get_cumulative_elapsed_time():", timer.get_cumulative_elapsed_time())
    # 0:00:02....


def main():
    basic_example()
    print()
    basic_context_manager_example()
    print()
    description_example()
    print()
    hide_starting_log_example()
    print()
    hide_ending_log_example()
    print()
    hide_all_logs_example()
    print()
    same_line_log_example()
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
