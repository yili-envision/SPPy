import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


from file_path_variables import *
from data.Calce_PL import funcs
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.eigen_func_exp import EigenFuncExp
from src.cycler.discharge import Discharge


# Calce data
df_exp = pd.read_csv("C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/FirstDischarge.csv")
df_exp = df_exp[df_exp['Current_Amp'] != 0]
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = -df_exp['Current_Amp'].to_numpy()


# Operating parameters
T = 298.15
V_min = 2.8
V_max = 4.2
num_cycles = 1
charge_current = 0
discharge_current = np.mean(I_exp)
rest_time = 30

# Modelling parameters
SOC_init_p, SOC_init_n = 0.41, 0.7568

# Setup battery components
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                        func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                        func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                        filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell.elec_n.max_conc = 29000
model = SPModel(isothermal=False, degradation=False)

# set-up solver and solve
cycler = Discharge(discharge_current=discharge_current, V_min=V_min)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
sol = solver.solve(cycler=cycler, verbose=True, t_increment=1)
print(sol.x_surf_p)

# Plot
# plt.plot(t_exp, V_exp)
# plt.plot(sol.t, sol.V)
# plt.show()
# sol.plot_tV()
sol.comprehensive_plot()