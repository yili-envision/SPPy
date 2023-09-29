import numpy as np

import SPPy
from SPPy.parameter_estimations.rough_estimations import GridSearch


# Operating parameters
I = 0.1
T = 298.15
V_min = 2.5
SOC_min = 0
SOC_max=1
SOC_LIB = 1
rest_time = 7200

# Modelling parameters
SOC_init_p, SOC_init_n = 0.43736824, 0.8136202  # from GA results

# Below are the parameters arrays containing the values for grid search
cell = SPPy.BatteryCell(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
array_R_p = np.array([cell.elec_p.R])
array_R_n = np.array([cell.elec_n.R])
array_c_pmax = np.array([cell.elec_p.max_conc])
array_c_nmax = np.array([cell.elec_n.max_conc])
array_D_p = np.linspace(0.11e-14, 0.19e-14, 5)
# array_D_p = np.array([1e-14])
# array_D_n = np.linspace(10e-14, 50e-14, 5)
array_D_n = np.array([10e-14])

# Create battery cell and cycler instance
dc = SPPy.DischargeRest(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB, rest_time=rest_time,
                        SOC_LIB_max=SOC_min)
cell = SPPy.BatteryCell(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# perform simulations on the parameters and store results
grid_search_instance = GridSearch(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                  T=T, i_cycler=dc)
grid_search_instance.generate_data(array_R_p=array_R_p, array_R_n=array_R_n,
                                   array_c_pmax=array_c_pmax, array_c_nmax=array_c_nmax,
                                   array_D_p=array_D_p, array_D_n=array_D_n,
                                   save_results=True, index_start=36, dir_name='grid_search_results_dischargerest')

