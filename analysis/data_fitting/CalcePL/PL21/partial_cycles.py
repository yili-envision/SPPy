import pandas as pd
import matplotlib.pyplot as plt

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.cycler.cc import CCNoFirstRest

from SPPy.solution import Solution
from SPPy.visualization.plots import Plots
from funcs import correct_time

# Calce data
cycle_num_exp = 3
df_exp = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/First50PartialCycles.csv')
df_exp = df_exp[df_exp['Cycle']==cycle_num_exp]
t_init = df_exp['Time_sec'].iloc[0]
df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
cycle_exp = df_exp['Cycle']
step_exp = df_exp["Step"]
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = df_exp['Current_Amp'].to_numpy()
cap_charge_exp = df_exp['Charge_Ah'].to_numpy()
cap_discharge_exp = df_exp['Discharge_Ah'].to_numpy()

print(df_exp.columns)

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
# SOC_init_p, SOC_init_n = 0.9030092608479767, 0.13857156903558143 # ga results for V-terminated
SOC_init_p, SOC_init_n = 0.852422478611043, 0.085 # ga results for SOC-terminated
# SOC_init_p, SOC_init_n = 0.8459567069686155, 0.12948510722779538 # ga results for SOC-terminated
# SOC_init_p, SOC_init_n = 0.952422478611043, 0.01973244470098207 # manual

# Setup battery components and model with the results from genetic algorithm
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                   func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                   filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
# cell.cap= 1.45
print(cell.cap)
# cell.R_cell = 0.07592084995520199 # ga results for V-terminated
cell.R_cell = 0.06230465601788312 # ga results for SOC-terminated
# cell.R_cell = 0.01 # manual
# cell.elec_p.max_conc, cell.elec_n.max_conc = 39467.385643904636, 37253.22610498574 # ga results for V-terminated
# cell.elec_p.max_conc, cell.elec_n.max_conc = 41304.90683917886, 37145.25756165516 # ga results for SOC-terminated
cell.elec_p.max_conc, cell.elec_n.max_conc = 47000, 25000 # manual
# cell.elec_p.R = 5e-6
model = SPModel(isothermal=False, degradation=False)

# set-up solver and solve
cycler = CCNoFirstRest(num_cycles=num_cycles, charge_current=charge_current, discharge_current=discharge_current,
                       rest_time=rest_time, V_max=V_max, V_min=V_min, SOC_min=0.2, SOC_max=0.8, SOC_LIB=0.2)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
sol = solver.solve(sol_name = "sim",cycler=cycler, verbose=False, t_increment=t_increment, termination_criteria = 'SOC')

# # plots
Plots(sol_exp, sol).plot_tV()
sol.comprehensive_plot()
