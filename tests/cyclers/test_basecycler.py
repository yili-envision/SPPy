import unittest

from src.cycler.base import BaseCycler


class TestBaseCycler(unittest.TestCase):
    def test_constructor(self):
        bc = BaseCycler()
        self.assertEqual(0.0, bc.time_elapsed)
