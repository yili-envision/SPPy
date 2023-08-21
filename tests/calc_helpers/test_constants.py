import unittest
from SPPy.calc_helpers import constants


class TestConstants(unittest.TestCase):

    def test_constants(self):
        """
        This test method test the constants defined in the Constants class.
        """
        self.assertEqual(constants.Constants.F, 96487)
        self.assertEqual(constants.Constants.R, 8.3145)
        self.assertEqual(constants.Constants.T_abs, 273.15)