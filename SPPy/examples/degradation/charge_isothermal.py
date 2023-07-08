import matplotlib.pyplot as plt

from SPPy.examples.file_path_variables import *
from data.test import funcs
import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_max = 4.2
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.989011, 0.01890232  # conditions in the literature source. Guo et al.

# Setup battery components
cell1 = SPPy.BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                        func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                        func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                        filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)

# set-up cycler and solver
cc = SPPy.Charge(charge_current=I, V_max=V_max)
solver1 = SPPy.SPPySolver(b_cell= cell1, N=5, isothermal=True, degradation=True)

# simulate
sol1 = solver1.solve(cycler=cc)

# Plot
sol1.plot_SEI()
