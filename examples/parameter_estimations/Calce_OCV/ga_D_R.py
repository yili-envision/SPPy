import numpy as np

from extract_exp_data import *
from parameter_sets.Calce_NMC_18650.funcs import OCP_ref_n, OCP_ref_p

import SPPy
from SPPy.calc_helpers.optimizations import GA
from OCP import OCV, func_OCV_exp, mse


def func_obj(lst_param: list):
    # Operating parameters
    I = 0.1
    T = 298.15
    V_min = 2.5
    SOC_min = 0
    SOC_LIB = 1

    # Modelling parameters
    SOC_n_min = 0.01098666
    SOC_n_max = 0.7953467
    SOC_p_min = 0.43144714
    SOC_p_max = 0.90469321

    SOC_init_p, SOC_init_n = SOC_p_min, SOC_n_max  # from GA results

    # Setup battery components
    cell = SPPy.BatteryCell(parameter_set_name='Calce_NMC_18650', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
    # cell.elec_n.D_ref = lst_param[0]
    cell.elec_n.R = lst_param[0]
    # cell.elec_p.D_ref = lst_param[2]
    cell.elec_p.R = lst_param[1]

    # set-up cycler and solver
    dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

    sol = solver.solve(cycler_instance=dc, t_increment=1) # simulate
    try:
        return (sol.x_surf_n[-1] - SOC_n_min) ** 2 + (sol.x_surf_p[-1] - SOC_p_max) ** 2
    except:
        return 1000


obj_ga = GA(n_chromosomes=10, bounds=np.array([[11e-6, 14e-6], [7.5e-6, 9e-6]]),
            obj_func=func_obj,
            n_pool=7, n_elite=3,
            n_generations=2)
array_param,_ = obj_ga.solve()

# print(array_param, OCV(array_chromosome=array_param))