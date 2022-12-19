import unittest

from file_path_variables import *
from data.test import funcs
from src.battery_components import battery_cell
from src.models import single_particle_model


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
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
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