import numpy as np
import matplotlib.pyplot as plt

from file_path_variables import *
from data.test import funcs
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.FD import FiniteDifferences


# Operating parameters
t = np.arange(0, 4000, 1)
I = -1.656 * np.ones(len(t))
T = 298.15

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                        func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                        func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                        filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
model = SPModel(isothermal=True, degradation=False)

# set-up solver and solve
solver = FiniteDifferences(b_cell= cell, b_model= model, N=5, t= t, I= I)
c_n = solver.solve()
#
# # Plot
# sol.comprehensive_plot()

plt.plot(c_n)
plt.show()