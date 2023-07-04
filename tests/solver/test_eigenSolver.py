import unittest
import numpy as np

from tests.test_config.file_path_variables import *
from data.test import funcs
from SPPy import BatteryCell, SPModel, EigenFuncExp, Discharge


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

    def test_solve_uk(self):
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
        u_k_p = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[0], t_prev=0, u_k_j_prev=0,
                                        scaled_j=0.253363842, dt=1, electrode_type='p')
        u_k_p1 = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[1], t_prev=0, u_k_j_prev=0,
                                         scaled_j=0.253363842, dt=1, electrode_type='p')
        u_k_p2 = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[2], t_prev=0, u_k_j_prev=0,
                                         scaled_j=0.253363842, dt=1, electrode_type='p')
        u_k_p3 = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[3], t_prev=0, u_k_j_prev=0,
                                         scaled_j=0.253363842, dt=1, electrode_type='p')
        u_k_p4 = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[4], t_prev=0, u_k_j_prev=0,
                                         scaled_j=0.253363842, dt=1, electrode_type='p')
        u_k_n = test_solver.solve_u_k_j(root_value=test_solver.lambda_roots[0], t_prev=0, u_k_j_prev=0,
                                        scaled_j=-0.220837089, dt=1, electrode_type='n')
        self.assertEqual(u_k_p, 7.003741197165458e-05)
        self.assertEqual(6.98464516914448e-05, u_k_p1)
        self.assertEqual(u_k_p2, 6.956137329676274e-05)
        self.assertEqual(u_k_p3, 6.918369224531671e-05)
        self.assertEqual(u_k_p4, 6.871543790445426e-05)
        self.assertEqual(u_k_n, -0.00010996455308935178)

    def test_summation_term(self):
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
        u_k_p = u_k_n = np.zeros(N)
        u_k_p, u_k_n, sum_term_p, sum_term_n = test_solver.get_summation_term(t_prev=0, dt=1,
                                                                              u_k_p=u_k_p,
                                                                              u_k_n=u_k_n,
                                                                              scaled_j_p=0.253363842,
                                                                              scaled_j_n=-0.220837089)
        # test u_k_p
        self.assertEqual(-4.027921416876962e-05, u_k_p[0])
        self.assertEqual(-4.061112545167694e-05, u_k_p[1])
        self.assertEqual(-4.109478647714362e-05, u_k_p[2])
        self.assertEqual(-4.171393978750682e-05, u_k_p[3])
        self.assertEqual(-4.244782133688522e-05, u_k_p[4])
        # summation terms
        self.assertEqual(-0.041772107048934325, sum_term_p)
        self.assertEqual(0.036506025487382576, sum_term_n)

    def test_calc_V(self):
        N = 5
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        I = 1.656
        T = 298.15
        V_min = 4.0
        SOC_min = 0.1
        SOC_LIB = 0.9
        test_cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                                func_dOCPdT_p=funcs.dOCPdT_p, filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                                func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                                filepath_electrolyte=TEST_ELECTROLYTE_DIR, filepath_cell=TEST_BATTERY_CELL_DIR, T=T)
        test_model = SPModel(isothermal=True, degradation=False)
        test_solver = EigenFuncExp(b_cell=test_cell, b_model=test_model, N=N)
        dc = Discharge(discharge_current=I, V_min=V_min, SOC_min=SOC_min, SOC_LIB=SOC_LIB)
        sol = test_solver.solve(cycler=dc)
        self.assertEqual(4.017944458468085, sol.V[0])
        self.assertEqual(4.0178735493136415, sol.V[1])
        self.assertEqual(4.01780271676398, sol.V[2])
        self.assertEqual(4.017731960073281, sol.V[3])
        self.assertEqual(4.017661278502599, sol.V[4])