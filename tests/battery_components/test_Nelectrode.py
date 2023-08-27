import unittest

from SPPy.battery_components import electrode
from tests.test_config.file_path_variables import TEST_NEG_ELEC_DIR # imports the test positive electrode's csv file path.
from parameter_sets.test import funcs  # imports the test OCP vs. SOC function and dOCP/dT functions


class TestNElectrode(unittest.TestCase):
    T = 298.15
    SOC_init = 0.59
    A_n = 0.0596
    L_n = 7.35e-5
    kappa_n = 100
    epsilon_n = 0.59
    S_n = 0.7824
    max_conc_n = 31833
    R_n = 12.5e-6
    k_ref_n = 1.76e-11
    D_ref_n = 3.9e-14
    Ea_R_n = 2e4
    Ea_D_n = 3.5e4
    alpha_n = 0.5
    T_ref_n = 298.15
    brugg_n = 1.5
    n_elec = electrode.NElectrode(L=L_n, A=A_n, kappa=kappa_n, epsilon=epsilon_n, S=S_n, max_conc=max_conc_n,
                                  R=R_n, k_ref=k_ref_n, D_ref=D_ref_n, Ea_R=Ea_R_n, Ea_D=Ea_D_n, alpha=alpha_n,
                                  T_ref=T_ref_n, brugg=brugg_n, SOC_init=SOC_init, func_OCP=funcs.OCP_ref_n,
                                  func_dOCPdT=funcs.dOCPdT_n, T=298.15)

    def test_NElectrode(self):
        """
        This test methods ensures that the NElectrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        """
        self.assertEqual(self.n_elec.L, 7.35e-05)
        self.assertEqual(self.n_elec.A, 5.960000e-02)
        self.assertEqual(self.n_elec.max_conc, 31833)
        self.assertEqual(self.n_elec.epsilon, 0.59)
        self.assertEqual(self.n_elec.kappa, 100)
        self.assertEqual(self.n_elec.S, 0.7824)
        self.assertEqual(self.n_elec.R, 12.5e-6)
        self.assertEqual(self.n_elec.T_ref, 298.15)
        self.assertEqual(self.n_elec.D_ref, 3.9e-14)
        self.assertEqual(self.n_elec.k_ref, 1.76e-11)
        self.assertEqual(self.n_elec.Ea_D, 35000)
        self.assertEqual(self.n_elec.Ea_R, 20000)
        self.assertEqual(self.n_elec.brugg, 1.5)
        self.assertEqual(self.n_elec.T, 298.15)
        self.assertEqual(self.n_elec.SOC, self.SOC_init)
        self.assertEqual(self.n_elec.electrode_type, 'n')

        # # Test for SEI related attributes
        # self.assertEqual(0.4, self.n_elec.U_s)
        # self.assertEqual(1.5e-6, self.n_elec.i_s)
        # self.assertEqual(0.16, self.n_elec.MW_SEI)
        # self.assertEqual(1600, self.n_elec.rho_SEI)
        # self.assertEqual(5e-6, self.n_elec.kappa_SEI)

    def test_OCP_values(self):
        """
        This test method ensures that the OCP are calculated correctly from the inputted OCP values.
        :return:
        """
        T = 298.15
        SOC_init = 0.7568
        self.n_elec.T = T
        self.n_elec.SOC = SOC_init
        self.assertEqual( 0.07464309895951012, self.n_elec.OCP)