import unittest

from SPPy.battery_components import electrolyte
from tests.test_config.file_path_variables import TEST_ELECTROLYTE_DIR, TEST_ELECTROLYTE_ERROR_DIR


class TestElectrolyte(unittest.TestCase):
    L = 2e-5
    c_init = 1000.0
    kappa = 0.2875
    epsilon = 0.724
    brugg = 1.5
    test_electrolyte = electrolyte.Electrolyte(L=L, conc=c_init, kappa=kappa, brugg=brugg, epsilon=epsilon)

    def test_constructor(self):
        """
        This test checks if the constructor of the Electrolyte class is able to read the parameters from the csv file
        and assign the class attributes correctly.
        """
        self.assertEqual(self.c_init, self.test_electrolyte.conc)
        self.assertEqual(self.L, self.test_electrolyte.L)
        self.assertEqual(self.kappa, self.test_electrolyte.kappa)
        self.assertEqual(self.epsilon, self.test_electrolyte.epsilon)
        self.assertEqual(self.brugg, self.test_electrolyte.brugg)

    def test_property(self):
        self.assertEqual(0.1771110665373567, self.test_electrolyte.kappa_eff)

    def test_constructur_raises(self):
        with self.assertRaises(TypeError) as context:
            electrolyte.Electrolyte(TEST_ELECTROLYTE_ERROR_DIR)