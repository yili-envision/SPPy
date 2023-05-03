import numpy as np
import pandas as pd

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.eigen_func_exp import EigenFuncExp
from src.cycler.charge import Charge

from src.solution import Solution
from src.visualization.plots import Plots
from funcs import correct_time


# Calce data
cycle_num_exp = 5
df_exp = pd.read_csv(CSV_EXP_FILE)
df_exp = df_exp[df_exp['Cycle']==cycle_num_exp]
print(np.unique(df_exp['Step']))
df_exp = df_exp[df_exp['Step']==7]
t_init = df_exp['Time_sec'].iloc[0]
# df_exp = df_exp[df_exp['Cycle']==cycle_num_exp]
# df_exp = df_exp[df_exp['Step']==7]
df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
cycle_exp = df_exp['Cycle']
step_exp = df_exp["Step"]
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = df_exp['Current_Amp'].to_numpy()
cap_charge_exp = df_exp['Charge_Ah'].to_numpy()
cap_discharge_exp = df_exp['Discharge_Ah'].to_numpy()

sol_exp = Solution(name = "exp", cycle_num=cycle_exp, cycle_step=step_exp, t=t_exp, I=I_exp, V=V_exp, cap_charge=cap_charge_exp,
                   cap_discharge=cap_discharge_exp, T=None, x_surf_p=None, x_surf_n=None,cap=None, R_cell=None,
                   battery_cap=1.45)

# Operating parameters
T = 298.15
V_min = 3.6
V_max = 4.2
num_cycles = 1
charge_current = 0.75
discharge_current = 0.75
rest_time = 1795

# Modelling parameters
t_increment = 1
SOC_init_p, SOC_init_n = 0.975, 0.00012 # manual

# Setup battery components and model with the results from genetic algorithm
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                   func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                   filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell.R_cell = 0.06230465601788312 # parameters from PL21
cell.elec_p.max_conc, cell.elec_n.max_conc = 47000, 25000 # parameters from PL21
model = SPModel(isothermal=False, degradation=False)

# set-up solver and solve
cycler = Charge(charge_current=charge_current, V_max=V_max, SOC_max=0.6, SOC_LIB=0)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
sol = solver.solve(sol_name = "sim",cycler=cycler, verbose=False, t_increment=t_increment, termination_criteria = 'SOC')

# # plots
Plots(sol_exp, sol).plot_tV()
# sol.comprehensive_plot()