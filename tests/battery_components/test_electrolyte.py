import unittest

from SPPy.battery_components import electrolyte
from file_path_variables import TEST_ELECTROLYTE_DIR


class TestElectrolyte(unittest.TestCase):

    def test_constructor(self):
        """
        This test checks if the constructor of the Electrolyte class is able to read the parameters from the csv file
        and assign the class attributes correctly.
        """
        test_electrolyte = electrolyte.Electrolyte(TEST_ELECTROLYTE_DIR)
        self.assertEqual(test_electrolyte.conc, 1000)
        self.assertEqual(test_electrolyte.L, 2e-5)
        self.assertEqual(test_electrolyte.kappa, 0.2875)
        self.assertEqual(test_electrolyte.epsilon, 0.724)
        self.assertEqual(test_electrolyte.brugg, 1.5)