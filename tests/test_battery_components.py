import unittest

from file_path_variables import *
from src.battery_components import electrode, electrolyte, battery_cell
from data.test import funcs
from src.warnings_and_exceptions import custom_exceptions


class TestElectrode(unittest.TestCase):

    def test_constructor(self):
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

    def test_invalid_SOC_init(self):
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
        T = 298.15
        SOC_init = 0.59
        elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                   func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(elec.SOC, SOC_init)
        # Now change the SOC
        new_SOC = 0.71
        elec.SOC = new_SOC
        self.assertEqual(elec.SOC, new_SOC)
        # Now change it to invalid SOC
        new_SOC = -1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            elec.SOC = new_SOC
        # Now change it to another invalid SOC
        new_SOC = 1.1
        with self.assertRaises(custom_exceptions.InvalidSOCException):
            elec.SOC = new_SOC

    def test_invalid_func_OCP_input(self):
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError) as context_manager:
            elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP= 13,
                                       func_dOCPdT=funcs.dOCPdT_p)

    def test_invalid_func_dOCPdT_input(self):
        T = 298.15
        SOC_init = 0.59
        with self.assertRaises(TypeError):
            elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                       func_dOCPdT=13)


class TestPElectrode(unittest.TestCase):

    def test_constructor(self):
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
        self.assertEqual(pelec.electrode_type,'p')

    def test_diffusivity(self):
        # Test at room temperature (which also happens to be the reference temperature)
        T = 298.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.D, 1e-14)

        # Test at above room temperature
        T = 313.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.D, 1.75130006059155e-14)
        # Test at below room temperature
        T = 288.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.D, 6.663211371340228e-15)

    def test_rate_constant(self):
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
        T = 298.15
        SOC_init = 0.4956
        p_elec = electrode.Electrode(file_path=TEST_POS_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_p,
                                     func_dOCPdT=funcs.dOCPdT_p)
        self.assertEqual(p_elec.OCP, 4.176505962016067)


class TestNElectrode(unittest.TestCase):

    def test_NElectrode(self):
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
        T = 298.15
        SOC_init = 0.7568
        n_elec = electrode.NElectrode(file_path=TEST_NEG_ELEC_DIR, SOC_init=SOC_init, T=T, func_OCP=funcs.OCP_ref_n,
                                      func_dOCPdT=funcs.OCP_ref_p)
        self.assertEqual(n_elec.OCP, 0.07464309895951012)


class TestElectrolyte(unittest.TestCase):

    def test_constructor(self):
        test_electrolyte = electrolyte.Electrolyte(TEST_ELECTROLYTE_DIR)
        self.assertEqual(test_electrolyte.conc, 1000)
        self.assertEqual(test_electrolyte.L, 2e-5)
        self.assertEqual(test_electrolyte.kappa, 0.2875)
        self.assertEqual(test_electrolyte.epsilon, 0.724)
        self.assertEqual(test_electrolyte.brugg, 1.5)


class TestBatteryCell(unittest.TestCase):

    def test_constructor(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR,
                                             T=T)
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
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=T)
        self.assertEqual(test_cell.R_cell,1.0027761335385129e-05)

    def test_T(self):
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



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])
    unittest.TextTestRunner(verbosity=3).run(suite)