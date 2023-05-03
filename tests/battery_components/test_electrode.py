import unittest

from src.battery_components import electrode
from file_path_variables import TEST_POS_ELEC_DIR # imports the test positive electrode's csv file path.
from data.test import funcs # imports the test OCP vs. SOC function and dOCP/dT functions
from src.warnings_and_exceptions import custom_exceptions


class testElectrode(unittest.TestCase):
    def test_Electrode_constructor(self):
        """
        This test methods ensures that the Electrode object is created correctly, i.e., the csv is read correctly
        and assigned to relevant instance attributes.
        """
        T = 298.15
        SOC_init = 0.59
        elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                   func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(elec.L, 7.000000e-05)
        self.assertEqual(elec.A, 5.960000e-02)
        self.assertEqual(elec.max_conc, 51410)
        self.assertEqual(elec.epsilon, 0.49)
        self.assertEqual(elec.kappa, 3.8)
        self.assertEqual(elec.S, 1.1167)
        self.assertEqual(elec.R, 8.5e-6)
        self.assertEqual(elec.T_ref, 298.15)
        self.assertEqual(elec.D_ref, 1e-14)
        self.assertEqual(elec.k_ref, 6.67e-11)
        self.assertEqual(elec.Ea_D, 29000)
        self.assertEqual(elec.Ea_R, 58000)
        self.assertEqual(elec.brugg, 1.5)
        self.assertEqual(elec.T, 298.15)
        self.assertEqual(elec.SOC, SOC_init)
        self.assertEqual(elec.electrode_type, 'none')

    def test_invalid_SOC_init(self):
        """
        This test method checks if the constructor raises an InvalidSOCException when invalid SOC_init is passed.
        """
        T = 298.15
        # Check with a SOC below lower threshold
        SOC_init = -1
        self.assertRaises(custom_exceptions.InvalidSOCException, electrode.Electrode, TEST_POS_ELEC_DIR, SOC_init, T, funcs.OCP_ref_p,
                          funcs.dOCPdT_p)
        # Check with a SOC above upper threshold
        SOC_init = 1.2
        self.assertRaises(custom_exceptions.InvalidSOCException, electrode.Electrode, TEST_POS_ELEC_DIR, SOC_init, T, funcs.OCP_ref_p,
                          funcs.dOCPdT_p)

    def test_SOC_setter(self):
        """
        This test method checks if the SOC attribute of the Electrode object can be changes correctly.
        """
        T = 298.15
        SOC_init = 0.59
        elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                   func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(elec.SOC, SOC_init)
        # Now change the SOC
        new_SOC = 0.71
        elec.SOC = new_SOC
        self.assertEqual(elec.SOC, new_SOC)
        # Now change it to invalid SOC, i.e, SOC < 0
        new_SOC = -1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            elec.SOC = new_SOC
        # Now change it to another invalid SOC, i.e, SOC > 1
        new_SOC = 1.1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            elec.SOC = new_SOC

    def test_invalid_func_OCP_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_OCP parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError) as context_manager:
            # Create an instance of Electrode object using a value (instead of a valid function) for func_OCP parameter.
            electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP= 13,
                                func_dOCPdT=funcs.dOCPdT_p)

    def test_invalid_func_dOCPdT_input(self):
        """
        This test method checks if the constructor raises a TypeError when an invalid function is passed for the
        func_dOCPdT parameter.
        """
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError):
            # Create an instance of the Electrode object using a value (instead of a valid function) for func_dOCPdT
            # parameter.
            electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                func_dOCPdT=13)
