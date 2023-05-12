import numpy as np

from file_path_variables import *
from data.test import funcs
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.visualization.plots import Plots


# Operating parameters
t = np.arange(0, 4500, 0.1)
I = -1.656 * np.ones(len(t))
T = 298.15

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components and model
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                    func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                    filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
model = SPModel(isothermal=True, degradation=False)
cell1 = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                    func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                    filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell1.elec_p.max_conc = 50000
model1 = SPModel(isothermal=True, degradation=False)
cell2 = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                    func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                    filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell2.elec_p.max_conc = 53000
model2 = SPModel(isothermal=True, degradation=False)

# set-up solver and solve
solver = EigenFuncExp(b_cell= cell, b_model= model, N=5, t= t, I= I)
sol = solver.solve("cs_max = 51555 mol/m3")
solver1 = EigenFuncExp(b_cell= cell1, b_model= model1, N=5, t= t, I= I)
sol1 = solver1.solve("cs_max = 50000 mol/m3")
solver2 = EigenFuncExp(b_cell= cell2, b_model= model2, N=5, t= t, I= I)
sol2 = solver2.solve("cs_max = 53000 mol/m3")

# Plot
Plots(sol, sol1, sol2).comprehensive_plot()