import unittest

import SPPy


class TestBatteryCell(unittest.TestCase):
    T = 298.15
    SOC_init_p = 0.4956
    SOC_init_n = 0.7568
    test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

    def test_negative_electrode_parameters(self):
        """
        This test method test the constructor of the BatteryCell class.
        """
        # Below tests for the negative electrode parameters
        self.assertEqual(self.test_cell.elec_n.L, 7.35e-05)
        self.assertEqual(self.test_cell.elec_n.A, 5.960000e-02)
        self.assertEqual(self.test_cell.elec_n.max_conc, 31833)
        self.assertEqual(self.test_cell.elec_n.epsilon, 0.59)
        self.assertEqual(self.test_cell.elec_n.kappa, 100)
        self.assertEqual(self.test_cell.elec_n.S, 0.7824)
        self.assertEqual(self.test_cell.elec_n.R, 12.5e-6)
        self.assertEqual(self.test_cell.elec_n.T_ref, 298.15)
        self.assertEqual(self.test_cell.elec_n.D_ref, 3.9e-14)
        self.assertEqual(self.test_cell.elec_n.k_ref, 1.76e-11)
        self.assertEqual(self.test_cell.elec_n.Ea_D, 35000)
        self.assertEqual(self.test_cell.elec_n.Ea_R, 20000)
        self.assertEqual(self.test_cell.elec_n.brugg, 1.5)
        self.assertEqual(self.test_cell.elec_n.T, 298.15)
        self.assertEqual(self.test_cell.elec_n.SOC, self.SOC_init_n)
        self.assertEqual(self.test_cell.elec_n.electrode_type, 'n')

    def test_electrolyte_parameters(self):
        # Below tests for the electrolyte parameters
        self.assertEqual(self.test_cell.electrolyte.conc, 1000)
        self.assertEqual(self.test_cell.electrolyte.L, 2e-5)
        self.assertEqual(self.test_cell.electrolyte.kappa, 0.2875)
        self.assertEqual(self.test_cell.electrolyte.epsilon, 0.724)
        self.assertEqual(self.test_cell.electrolyte.brugg, 1.5)

    def test_battery_cell_parameters(self):
        # below tests for the battery cell parameters
        self.assertEqual(self.test_cell.rho, 1626)
        self.assertEqual(self.test_cell.Vol, 3.38e-5)
        self.assertEqual(self.test_cell.C_p, 750)
        self.assertEqual(self.test_cell.h, 1)
        self.assertEqual(self.test_cell.A, 0.085)
        self.assertEqual(self.test_cell.cap, 1.65)
        self.assertEqual(self.test_cell.V_max, 4.2)
        self.assertEqual(self.test_cell.V_min, 2.5)

    def test_R_cell(self):
        self.assertEqual(0.0028230038442483246, self.test_cell.R_cell)

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


class TestECMBatteryCell:
    test_cell = SPPy.ECMBatteryCell(R0=0.225, R1=0.001, C1=0.03, T_=298.15, rho=1626, Vol=3.38e-5, C_p=750, h=1, A=0.085,
                                    cap=1.65, V_max=4.2, V_min=2.5)

    def test_battery_cell_parameters(self):
        self.assertEqual(self.test_cell.rho, 1626)
        self.assertEqual(self.test_cell.Vol, 3.38e-5)
        self.assertEqual(self.test_cell.C_p, 750)
        self.assertEqual(self.test_cell.h, 1)
        self.assertEqual(self.test_cell.A, 0.085)
        self.assertEqual(self.test_cell.cap, 1.65)
        self.assertEqual(self.test_cell.V_max, 4.2)
        self.assertEqual(self.test_cell.V_min, 2.5)
