import unittest

from SPPy.battery_components import electrode
from tests.test_config.file_path_variables import TEST_NEG_ELEC_DIR # imports the test positive electrode's csv file path.
from data.test import funcs # imports the test OCP vs. SOC function and dOCP/dT functions


class TestNElectrode(unittest.TestCase):

    def test_NElectrode(self):
        """
        This test methods ensures that the NElectrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        """
        T = 298.15
        SOC_init = 0.59
        n_elec = electrode.NElectrode(file_path=TEST_NEG_ELEC_DIR, SOC_init=SOC_init,T=T, func_OCP=funcs.OCP_ref_n,
                                      func_dOCPdT=funcs.OCP_ref_p)
        self.assertEqual(n_elec.L, 7.35e-05)
        self.assertEqual(n_elec.A, 5.960000e-02)
        self.assertEqual(n_elec.max_conc, 31833)
        self.assertEqual(n_elec.epsilon, 0.59)
        self.assertEqual(n_elec.kappa, 100)
        self.assertEqual(n_elec.S, 0.7824)
        self.assertEqual(n_elec.R, 12.5e-6)
        self.assertEqual(n_elec.T_ref, 298.15)
        self.assertEqual(n_elec.D_ref, 3.9e-14)
        self.assertEqual(n_elec.k_ref, 1.76e-11)
        self.assertEqual(n_elec.Ea_D, 35000)
        self.assertEqual(n_elec.Ea_R, 20000)
        self.assertEqual(n_elec.brugg, 1.5)
        self.assertEqual(n_elec.T, 298.15)
        self.assertEqual(n_elec.SOC, SOC_init)
        self.assertEqual(n_elec.electrode_type, 'n')

    def test_OCP_values(self):
        """
        This test method ensures that the OCP are calculated correctly from the inputted OCP values.
        :return:
        """
        T = 298.15
        SOC_init = 0.7568
        n_elec = electrode.NElectrode(file_path=TEST_NEG_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_n,
                                      func_dOCPdT=funcs.OCP_ref_p)
        self.assertEqual(n_elec.OCP, 0.07464309895951012)