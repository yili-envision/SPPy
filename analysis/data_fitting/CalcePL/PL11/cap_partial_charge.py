import pandas as pd
import matplotlib.pyplot as plt

# from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.cycler.cc import CCNoFirstRest


# Calce data
df_exp = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL11/First100cycles.csv')

# all cycle numbers
cycle_no_list = df_exp['Cycle'].unique()

cap_list = []
for cycle_no_ in range(2,cycle_no_list[-1]):
    current_dis_cap = df_exp[(df_exp['Cycle']==cycle_no_) & (df_exp['Step']==8)].iloc[-1]['Discharge_Ah']
    prev_dis_cap = df_exp[(df_exp['Cycle'] == cycle_no_-1) & (df_exp['Step'] == 8)].iloc[-1]['Discharge_Ah']
    cap_list.append(current_dis_cap - prev_dis_cap)

plt.scatter(cycle_no_list[2:], cap_list)
plt.show()