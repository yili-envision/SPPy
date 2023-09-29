import numpy as np

import SPPy
from SPPy.parameter_estimations.rough_estimations import GridSearch


# Operating parameters
I = 0.1
T = 298.15
V_min = 2.5
SOC_min = 0
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.43736824, 0.8136202  # from GA results

# Below are the parameters arrays containing the values for grid search
# array_R_p = np.linspace(8.5e-6, 10e-6, 2)
# array_R_n = np.linspace(10e-6, 15e-6, 2)
# array_c_pmax = np.linspace(45000, 50000, 2)
# array_c_nmax = np.linspace(27500, 32000, 2)
array_R_p = np.array([8.5e-6])
array_R_n = np.linspace(16e-6, 18e-5, 3)
array_c_pmax = np.linspace(51000, 55000, 3)
array_c_nmax = np.linspace(32000, 35000, 3)

# Create battery cell and cycler instance
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
cell = SPPy.BatteryCell(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# perform simulations on the parameters and store results
grid_search_instance = GridSearch(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n,
                                  T=T, i_cycler=dc)
grid_search_instance.generate_data(array_R_p=array_R_p, array_R_n=array_R_n,
                                   array_c_pmax=array_c_pmax, array_c_nmax=array_c_nmax,
                                   save_results=True, index_start=805)

