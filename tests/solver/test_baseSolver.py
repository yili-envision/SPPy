import unittest
import numpy as np

from tests.test_config.file_path_variables import *
from data.test import funcs
from SPPy import BatteryCell, SPModel
from SPPy.solvers.base import BaseSolver


class TestBaseSolver(unittest.TestCase):

    def test_constructor(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        t = np.arange(0, 4000, 0.1)
        I = -1.656 * np.ones(len(t))
        test_cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                                func_dOCPdT_p=funcs.dOCPdT_p, filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                filepath_electrolyte=TEST_ELECTROLYTE_DIR, filepath_cell=TEST_BATTERY_CELL_DIR, T=T)
        test_model = SPModel(isothermal=False, degradation=False)
        with self.assertRaises(TypeError):
            BaseSolver(b_cell=test_cell, b_model=1, t=t, I=I)
        with self.assertRaises(TypeError):
            BaseSolver(b_cell=1, b_model=test_model, t=t, I=I)