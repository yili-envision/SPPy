import unittest
from src.calc_helpers import constants


class TestConstants(unittest.TestCase):

    def test_constants(self):
        self.assertEqual(constants.Constants.F, 96487)
        self.assertEqual(constants.Constants.R, 8.3145)