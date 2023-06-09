import unittest

from SPPy.battery_components import electrode
from tests.test_config.file_path_variables import TEST_POS_ELEC_DIR # imports the test positive electrode's csv file path.
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
        pelec = electrode.PElectrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
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
        self.assertEqual(pelec.SOC, SOC_init)
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
