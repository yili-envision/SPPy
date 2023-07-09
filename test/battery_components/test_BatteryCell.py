import unittest

import SPPy


class TestBatteryCell(unittest.TestCase):

    def test_constructor(self):
        """
        This test method test the constructor of the BatteryCell class.
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

        self.assertEqual(test_cell.rho, 1626)
        self.assertEqual(test_cell.Vol, 3.38e-5)
        self.assertEqual(test_cell.C_p, 750)
        self.assertEqual(test_cell.h, 1)
        self.assertEqual(test_cell.A, 0.085)
        self.assertEqual(test_cell.cap, 1.65)
        self.assertEqual(test_cell.V_max, 4.2)
        self.assertEqual(test_cell.V_min, 2.5)

    def test_R_cell(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

        self.assertEqual(0.0028230038442483246, test_cell.R_cell)

    def test_T(self):
        """
        This test method checks if the temperature is properly assigned to the object after the temperature
        parameter is changed.
        :return:
        """
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

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
        test_T_amb test if the ambient temperature stays constant even after temperature parameter change.
        """
        orig_T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=orig_T)

        self.assertEqual(test_cell.T_amb, orig_T)
        # Now change to new T but T_amb should not change
        new_T = 313.15
        test_cell.T = new_T
        self.assertEqual(test_cell.T_amb, orig_T)