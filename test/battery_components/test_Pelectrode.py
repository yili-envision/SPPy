import unittest

from SPPy.battery_components import electrode
from test.test_config.file_path_variables import TEST_POS_ELEC_DIR # imports the test positive electrode's csv file path.
from data.test import funcs # imports the test OCP vs. SOC function and dOCP/dT functions


class TestPElectrode(unittest.TestCase):

    def test_constructor(self):
        """
        This test methods ensures that the PElectrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        :return:
        """
        T = 298.15
        SOC_init = 0.59
        L_p = 7e-5
        A_p = 0.0596
        max_conc_p = 51410
        epsilon_p = 0.49
        kappa_p = 3.8
        S_p = 1.1167
        R_p = 8.5e-6
        T_ref_p = 298.15
        D_ref_p = 1e-14
        k_ref_p = 6.67e-11
        Ea_D_p = 2.9e4
        Ea_R_p = 58000
        brugg_p = 1.5
        T_p = 298.15
        electrode_type = 'p'

        pelec = electrode.PElectrode(L=7e-5, A=A_p, max_conc=max_conc_p, epsilon=epsilon_p, kappa=kappa_p, S=S_p, R=R_p,
                                     T_ref=T_ref_p, D_ref=D_ref_p, k_ref=k_ref_p, Ea_D=Ea_D_p, Ea_R=Ea_R_p,
                                     brugg=brugg_p, T=T_p, SOC_init=SOC_init, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p, alpha=0.5)


        self.assertEqual(pelec.L, 7.000000e-05)
        self.assertEqual(pelec.A, 5.960000e-02)
        self.assertEqual(pelec.max_conc, 51410)
        self.assertEqual(pelec.epsilon, 0.49)
        self.assertEqual(pelec.kappa, 3.8)
        self.assertEqual(pelec.S, 1.1167)
        self.assertEqual(pelec.R, 8.5e-6)
        self.assertEqual(pelec.T_ref, 298.15)
        self.assertEqual(pelec.D_ref, 1e-14)
        self.assertEqual(pelec.k_ref, 6.67e-11)
        self.assertEqual(pelec.Ea_D, 29000)
        self.assertEqual(pelec.Ea_R, 58000)
        self.assertEqual(pelec.brugg, 1.5)
        self.assertEqual(pelec.T, 298.15)
        self.assertEqual(pelec.SOC_init, SOC_init)
        self.assertEqual(SOC_init, pelec.SOC)
        self.assertEqual(pelec.electrode_type, 'p')

    def test_diffusivity(self):
        """
        This test method ensures that the diffusivity is calculated correctly.
        """
        # Test at room temperature
        T = 298.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.D, 1e-14)

        # Change temp. to be above room temperature. Expect the diffusivity to be higher than that at room
        # temperature due to Arrhenius equation.
        p_elec.T = 313.15
        self.assertEqual(p_elec.D, 1.75130006059155e-14)

        # Change temp. to be below room temperature. Expect the diffusivity to be lower than that at room temperature
        # due to Arrhenius equation.
        p_elec.T = 288.15
        self.assertEqual(p_elec.D, 6.663211371340228e-15)

    def test_rate_constant(self):
        """
        This test method ensures that the rate constant is calculated correctly.
        """
        # Test at above room temperature
        T = 313.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.k, 2.045723618786054e-10)

        # Test at below room temperature
        T = 288.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.k, 2.961372331469821e-11)

    def test_OCP_values(self):
        """
        This test method ensures that the open-circuit potential (OCP) values are calculated correctly from the user
        inputted OCP vs. SOC function.
        """
        T = 298.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.OCP, 4.176505962016067)
