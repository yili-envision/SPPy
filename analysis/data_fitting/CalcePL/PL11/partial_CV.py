import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.eigen_func_exp import EigenFuncExp
from src.cycler.charge import Charge

from analysis.data_fitting.CalcePL.PL21.funcs import correct_time

# Calce data
cycle_no_exp= 2
step_exp = 3

df_exp = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL11/First100Cycles.csv')
df_exp = df_exp[df_exp['Cycle']==cycle_no_exp]
df_exp = df_exp[df_exp['Step']== step_exp]
print(df_exp['Step'].unique())
t_init = df_exp['Time_sec'].iloc[0]
df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = df_exp['Current_Amp'].to_numpy()

print(np.mean(I_exp))


plt.plot(t_exp, I_exp)
plt.show()