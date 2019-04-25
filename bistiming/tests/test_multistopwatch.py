import unittest

from examples import multistopwatch_examples


class TestMultiStopwatch(unittest.TestCase):
    def test_multistopwatch_examples(self):
        multistopwatch_examples.main()
