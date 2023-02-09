import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# from file_path_variables import *
# from data.Calce_PL import funcs
# from data.general_OCP.LCO import OCP_ref_p
# from src.battery_components.battery_cell import BatteryCell
# from src.models.single_particle_model import SPModel
# from src.solvers.eigen_func_exp import EigenFuncExp
# from src.cycler.cc import CCNoFirstRest
#
# from funcs import correct_time
#
# def append_cap(df, cycle_no_list, cycle_list, cap_list):
#     for cycle_no_ in range(2, cycle_no_list[-1]):
#         try:
#             current_dis_cap = df[(df_exp1['Cycle'] == cycle_no_) & (df['Step'] == 8)].iloc[-1]['Discharge_Ah']
#             prev_dis_cap = df[(df['Cycle'] == cycle_no_ - 1) & (df['Step'] == 8)].iloc[-1]['Discharge_Ah']
#             cap_list.append(current_dis_cap - prev_dis_cap)
#             cycle_list.append(cycle_no_)
#         except:
#             pass
#     return cycle_list, cap_list
#
#
# # Calce data
# df_exp1 = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/First50PartialCycles.csv')
# df_exp2 = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/Second50PartialCycles.csv')
# df_exp3 = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/Last100PartialCycles.csv')
# df_exp2['Cycle'] = df_exp2['Cycle'].apply(lambda x: x+51)
# df_exp3['Cycle'] = df_exp3['Cycle'].apply(lambda x: x+102)
# # df_exp = df_exp1.append(df_exp2)
# # df_exp = df_exp.append(df_exp3)
#
# # all cycle numbers
# cycle_no_list1 = df_exp1['Cycle'].unique()
# cycle_no_list2 = df_exp2['Cycle'].unique()
# cycle_no_list3 = df_exp3['Cycle'].unique()
#
# cycle_list = []
# cap_list = []
# cycle_list, cap_list = append_cap(df_exp1, cycle_no_list1, cycle_list, cap_list)
# cycle_list, cap_list = append_cap(df_exp2, cycle_no_list2, cycle_list, cap_list)
# cycle_list, cap_list = append_cap(df_exp3, cycle_no_list3, cycle_list, cap_list)
#
#
# plt.scatter(cycle_list, cap_list)
# plt.show()

# from Saxena et al. 2016.Cycle life testing and modeling of graphite/LiCoO2 cells under different state of charge ranges. JPS

A = 3.708
b = 0.452
cycle_no = np.arange(0, 801)
NDC = 100.0 - A * (cycle_no/100)**b

plt.plot(cycle_no, NDC)
plt.show()