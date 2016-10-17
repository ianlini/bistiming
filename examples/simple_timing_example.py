from time import sleep
import logging

from bistiming import SimpleTimer


def main():
    print("[Example 1]")
    with SimpleTimer():
        sleep(1)

    print("\n[Example 2] timer with description")
    with SimpleTimer("Waiting"):
        sleep(1)

    print("\n[Example 3] timer without starting message")
    with SimpleTimer("Waiting", verbose_start=False):
        sleep(1)

    print("\n[Example 4] timer without ending message")
    with SimpleTimer("Waiting", verbose_end=False):
        sleep(1)

    print("\n[Example 5] rewrite the same line after ending")
    with SimpleTimer("Waiting", end_in_new_line=False):
        sleep(1)

    print("\n[Example 6] change the prefix")
    with SimpleTimer("Waiting", prefix="[bistimer] "):
        sleep(1)

    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] %(levelname)s: %(name)s: %(message)s")
    logger = logging.getLogger(__name__)

    print("\n[Example 7] use python logging module")
    with SimpleTimer("Waiting", logger=logger):
        sleep(1)

    print("\n[Example 8] use python logging module with different log level")
    with SimpleTimer("Waiting", logger=logger, logging_level=logging.DEBUG):
        sleep(1)


if __name__ == '__main__':
    main()
