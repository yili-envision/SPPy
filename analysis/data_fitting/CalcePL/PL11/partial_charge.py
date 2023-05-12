import pandas as pd
import matplotlib.pyplot as plt

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.cycler.charge import Charge

from analysis.data_fitting.CalcePL.PL21.funcs import correct_time

# Calce data
cycle_no_exp= 3
step_exp = 2

df_exp = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL11/First100Cycles.csv')
df_exp = df_exp[df_exp['Cycle']==cycle_no_exp]
df_exp = df_exp[df_exp['Step']== step_exp]
print(df_exp['Step'].unique())
t_init = df_exp['Time_sec'].iloc[0]
df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = df_exp['Current_Amp'].to_numpy()


# Operating parameters
T = 298.15
V_min = 3.6
V_max = 4.2
num_cycles = 1
charge_current = 0.75
discharge_current = 0.75
rest_time = 1795

# Modelling parameters
t_increment = 5
SOC_init_p, SOC_init_n = 0.975, 0.0012 # manual

# Setup battery components and model with the results from genetic algorithm
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                   func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                   filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell.R_cell = 0.06230465601788312 # parameters from PL21
cell.elec_p.max_conc, cell.elec_n.max_conc = 47000, 25000 # parameters from PL21
model = SPModel(isothermal=False, degradation=False)

# set-up solver and solve
cycler = Charge(charge_current=charge_current, V_max=V_max, SOC_max=1, SOC_LIB=0.0)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
sol = solver.solve(cycler=cycler, verbose=True, t_increment=t_increment, termination_criteria = 'V')
#
# # plots
plt.plot(t_exp, V_exp, label="exp")
plt.plot(sol.t, sol.V, label="sim")
plt.legend()
plt.show()
#
# # sol.comprehensive_plot()