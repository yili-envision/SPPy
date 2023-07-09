import unittest

from SPPy.battery_components import electrolyte
from test.test_config.file_path_variables import TEST_ELECTROLYTE_DIR, TEST_ELECTROLYTE_ERROR_DIR


class TestElectrolyte(unittest.TestCase):
    test_electrolyte = electrolyte.Electrolyte(TEST_ELECTROLYTE_DIR)
    def test_constructor(self):
        """
        This test checks if the constructor of the Electrolyte class is able to read the parameters from the csv file
        and assign the class attributes correctly.
        """
        self.assertEqual(1000, self.test_electrolyte.conc)
        self.assertEqual(2e-5, self.test_electrolyte.L)
        self.assertEqual(0.2875, self.test_electrolyte.kappa)
        self.assertEqual(0.724, self.test_electrolyte.epsilon)
        self.assertEqual(1.5, self.test_electrolyte.brugg)

    def test_property(self):
        self.assertEqual(0.1771110665373567, self.test_electrolyte.kappa_eff)

    def test_constructur_raises(self):
        with self.assertRaises(TypeError) as context:
            electrolyte.Electrolyte(TEST_ELECTROLYTE_ERROR_DIR)