import unittest

from file_path_variables import TEST_BATTERY_CELL_DIR, TEST_ELECTROLYTE_DIR, TEST_NEG_ELEC_DIR, TEST_POS_ELEC_DIR
from src.battery_components import battery_cell
from data.test import funcs


class TestBatteryCell(unittest.TestCase):

    def test_constructor(self):
        """
        This test method tests the constructor of the BatteryCell class.
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte = TEST_ELECTROLYTE_DIR,
                                             filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
        self.assertEqual(test_cell.rho, 1626)
        self.assertEqual(test_cell.Vol, 3.38e-5)
        self.assertEqual(test_cell.C_p, 750)
        self.assertEqual(test_cell.h, 1)
        self.assertEqual(test_cell.A, 0.085)
        self.assertEqual(test_cell.cap, 1.65)
        self.assertEqual(test_cell.V_max, 4.2)
        self.assertEqual(test_cell.V_min, 2.5)

    # def test_R_cell(self):
    #     T = 298.15
    #     SOC_init_p = 0.4956
    #     SOC_init_n = 0.7568
    #     test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
    #                                          func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
    #                                          filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
    #                                          func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
    #                                          filepath_electrolyte=TEST_ELECTROLYTE_DIR,
    #                                          filepath_cell=TEST_BATTERY_CELL_DIR,
    #                                          T=T)
    #     self.assertEqual(test_cell.R_cell,1.0027761335385129e-05)

    def test_T(self):
        """
        This test method checks if the temperature is properly assigned to the object after the temperature
        parameter is changed.
        :return:
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=T)
        self.assertEqual(test_cell.T, T)
        self.assertEqual(test_cell.elec_p.T, T)
        self.assertEqual(test_cell.elec_n.T, T)
        # change T and check if the battery and electrode temperature changes as well.
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T, new_T)
        self.assertEqual(test_cell.elec_p.T, new_T)
        self.assertEqual(test_cell.elec_n.T, new_T)

    def test_T_amb(self):
        """
        test_T_amb tests if the ambient temperature stays constant even after temperature parameter change.
        """
        orig_T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=orig_T)
        self.assertEqual(test_cell.T_amb, orig_T)
        # Now change to new T but T_amb should not change
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T_amb, orig_T)