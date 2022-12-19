import unittest
import numpy as np

from file_path_variables import *
from data.test import funcs
from src.warnings_and_exceptions.custom_exceptions import *
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.base import BaseSolver
from src.solvers.eigen_func_exp import EigenFuncExp


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
        with self.assertRaises(InsufficientInputOperatingConditions):
            BaseSolver(b_cell=test_cell, b_model=test_model, t=t)
        with self.assertRaises(InsufficientInputOperatingConditions):
            BaseSolver(b_cell=test_cell, b_model=test_model, I=I)
        with self.assertRaises(InsufficientInputOperatingConditions):
            BaseSolver(b_cell=test_cell, b_model=test_model)


class TestEigenExpSolver(unittest.TestCase):

    def test_constructor(self):
        T = 298.15
        N = 5
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        t = np.arange(0, 4000, 0.1)
        I = -1.656 * np.ones(len(t))
        test_cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                                func_dOCPdT_p=funcs.dOCPdT_p, filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                filepath_electrolyte=TEST_ELECTROLYTE_DIR, filepath_cell=TEST_BATTERY_CELL_DIR, T=T)
        test_model = SPModel(isothermal=True, degradation=False)
        test_solver = EigenFuncExp(b_cell=test_cell, b_model=test_model, N=N, t=t, I=I)
        self.assertEqual(test_solver.N, N)
        self.assertEqual(test_solver.b_cell, test_cell)
        self.assertEqual(test_solver.b_model, test_model)

    def test_lambda_roots(self):
        T = 298.15
        N = 5
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        t = np.arange(0, 4000, 0.1)
        I = -1.656 * np.ones(len(t))
        test_cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                                func_dOCPdT_p=funcs.dOCPdT_p, filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                filepath_electrolyte=TEST_ELECTROLYTE_DIR, filepath_cell=TEST_BATTERY_CELL_DIR, T=T)
        test_model = SPModel(isothermal=True, degradation=False)
        test_solver = EigenFuncExp(b_cell=test_cell, b_model=test_model, N=N, t=t, I=I)
        self.assertEqual(test_solver.lambda_roots[0], 4.493409457910043)
        self.assertEqual(test_solver.lambda_roots[1], 7.725251836937441)
        self.assertEqual(test_solver.lambda_roots[2], 10.904121659428089)
        self.assertEqual(test_solver.lambda_roots[3], 14.06619391283256)
        self.assertEqual(test_solver.lambda_roots[4], 17.220755271929562)