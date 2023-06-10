import unittest

from SPPy.cycler.base import BaseCycler


class TestBaseCycler(unittest.TestCase):
    def test_constructor(self):
        bc = BaseCycler()
        self.assertEqual(0.0, bc.time_elapsed)
        self.assertEqual(0.0, bc.SOC_LIB)

    def test_reset_time_elapsed(self):
        bc = BaseCycler(time_elapsed=10.0)
        self.assertEqual(10.0, bc.time_elapsed)
        bc.reset_time_elapsed() # resets the instance's time elapsed
        self.assertEqual(0.0, bc.time_elapsed)
