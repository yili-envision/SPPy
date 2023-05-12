import unittest

from file_path_variables import *
from data.test import funcs
from SPPy.battery_components import battery_cell
from SPPy.models import single_particle_model


class TestSPModel(unittest.TestCase):

    def test_constructor(self):
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
        test_model = single_particle_model.SPModel(isothermal=True, degradation=False)
        self.assertTrue(test_model.isothermal)
        self.assertFalse(test_model.degradation)

    def test_invalid_constructor_arguments(self):
        T = 298.15
        # SOC_init_p = 0.4956
        SOC_init_p = 0.6
        # SOC_init_n = 0.7568
        SOC_init_n = 0.7
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=T)
        with self.assertRaises(TypeError):
            single_particle_model.SPModel(isothermal=13, degradation=False)
        with self.assertRaises(TypeError):
            single_particle_model.SPModel(isothermal=True, degradation=13)

    def test_m(self):
        T = 298.15
        # SOC_init_p = 0.4956
        SOC_init_p = 0.6
        # SOC_init_n = 0.7568
        SOC_init_n = 0.7
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=T)
        testmodel = single_particle_model.SPModel(isothermal=False, degradation=False)
        self.assertEqual(-0.2893183331034342, testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc, test_cell.elec_p.SOC, test_cell.electrolyte.conc))
        self.assertEqual(-2.7018597575301726, testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc, test_cell.elec_n.SOC, test_cell.electrolyte.conc))

    def test_V(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        R_cell = 0.00148861
        I = -1.656
        test_cell = battery_cell.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p,
                                             func_OCP_p=funcs.OCP_ref_p, func_dOCPdT_p=funcs.dOCPdT_p,
                                             filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                             func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                             filepath_electrolyte=TEST_ELECTROLYTE_DIR,
                                             filepath_cell=TEST_BATTERY_CELL_DIR,
                                             T=T)
        testmodel = single_particle_model.SPModel(isothermal=False, degradation=False)
        OCP_p = test_cell.elec_p.OCP
        OCP_n = test_cell.elec_n.OCP
        m_p = testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc, test_cell.elec_p.SOC,
                    test_cell.electrolyte.conc)
        m_n = testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc, test_cell.elec_n.SOC, test_cell.electrolyte.conc)
        self.assertEqual(4.032392212009281, testmodel.calc_term_V(OCP_p, OCP_n, m_p, m_n, R_cell, T=T, I=I))
        # change SOC
        test_cell.elec_p.SOC = 0.6
        test_cell.elec_n.SOC = 0.6
        OCP_p = test_cell.elec_p.OCP
        OCP_n = test_cell.elec_n.OCP
        m_p = testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc,
                          test_cell.elec_p.SOC,
                          test_cell.electrolyte.conc)
        m_n = testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc,
                          test_cell.elec_n.SOC, test_cell.electrolyte.conc)
        self.assertEqual(3.8782812640647926, testmodel.calc_term_V(OCP_p, OCP_n, m_p, m_n, R_cell, T=T, I=I))
