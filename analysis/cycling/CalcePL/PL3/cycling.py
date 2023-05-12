import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.models.degradation import ROM_SEI
from SPPy.cycler.cc import CC,CCNoFirstRest

# Operating parameters
T = 298.15
V_min_partial = 2
V_max_partial = 4.5
num_cycles_partial = 8
charge_current = 0.75
discharge_current = 0.75
rest_time = 1795

# Modelling parameters
t_increment = 10
SOC_init_p, SOC_init_n = 0.975, 0.00012 # manual


# Setup battery components and model with the results from genetic algorithm
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                   func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                   filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell.elec_p.max_conc, cell.elec_n.max_conc = 47000, 25000 # manual
cell.R_cell = 0.06230465601788312
model = SPModel(isothermal=False, degradation=True)
SEI_model = ROM_SEI(bCell= cell, file_path= SEI_DIR, resistance_init=1e-8, thickness_init=0)
SEI_model.limiting_coefficient = 1.25e9

cycler_partial = cycler = CCNoFirstRest(num_cycles=num_cycles_partial, charge_current=charge_current, discharge_current=discharge_current,
                       rest_time=rest_time, V_max=V_max_partial, V_min=V_min_partial, SOC_min=0, SOC_max=0.6,
                                        SOC_LIB=0)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5, SEI_model=SEI_model)
battery_cap_init = cell.cap

# solve
sol_partial = solver.solve(cycler=cycler_partial, verbose=False, t_increment=t_increment, termination_criteria = 'SOC')

# # save cycling data
# pd.DataFrame({'Cycle_no': sol_partial.filter_cycle_nums(),
#               'NDC' :sol_partial.calc_battery_cap_array()/battery_cap_init}).to_csv("cycling_sim_data.csv", index=False)

# prints and plots
sol_partial.comprehensive_plot()
print('cycle:', sol_partial.cycle_num[-1], 'SEI_thickness: ', SEI_model.thickness)
mpl.rcParams['lines.linewidth'] = 3
plt.rc('axes', titlesize=15)
plt.rc('axes', labelsize=15)
plt.plot(sol_partial.filter_cycle_nums(), sol_partial.calc_battery_cap_array()/battery_cap_init, label="sim")
plt.xlabel('Cycle No.')
plt.ylabel('Normalized Discharge Capacity')
plt.title('NDC vs. cycle')
plt.legend()
plt.show()