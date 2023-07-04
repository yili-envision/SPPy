from file_path_variables import *
from data.test import funcs
import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                        func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                        func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                        filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
model = SPPy.SPModel(isothermal=True, degradation=False)

# set-up solver and solve
dc = SPPy.CustomDischarge(SOC_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.EigenFuncExp(b_cell= cell, b_model= model, N=5)
sol = solver.solve(cycler=dc)

# Plot
sol.comprehensive_plot()