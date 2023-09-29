import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from OCP import OCV
from SPPy.calc_helpers.optimizations import GA


"""
Description of the GITT file
1. The discharge GITT happens from cycle 2 to 9
    a. each of the cycles contains the discharge (step_index = 5) and rest (step_index = 6) steps.
"""


def tau(df_exp: pd.DataFrame, cycle_index: int):
    return df_exp[(df_exp['Cycle_Index'] == cycle_index) & (df_exp['Step_Index'] == 5)]['t [s]'].iloc[-1]


def delta_V_t_exp(df_exp: pd.DataFrame, cycle_index: int):
    V1 = df_exp[(df_exp['Cycle_Index'] == cycle_index - 1) & (df_exp['Step_Index'] == 6)]['V [V]'].iloc[-1]
    V2 = df_exp[(df_exp['Cycle_Index'] == cycle_index) & (df_exp['Step_Index'] == 5)]['V [V]'].iloc[-1]
    return V1 - V2


def delta_V_s(df_exp: pd.DataFrame, cycle_index: int):
    V1 = df_exp[(df_exp['Cycle_Index'] == cycle_index - 1) & (df_exp['Step_Index'] == 6)]['V [V]'].iloc[-1]
    V2 = df_exp[(df_exp['Cycle_Index'] == cycle_index) & (df_exp['Step_Index'] == 6)]['V [V]'].iloc[-1]
    return V1 - V2


def cap(df_exp: pd.DataFrame, cycle_index: int):
    return df_exp[(df_exp['Cycle_Index'] == cycle_index) & (df_exp['Step_Index'] == 6)]['cap_charge [Ahr]'].iloc[-1]

def delta_V_ti(D: float, delta_V_s: float, tau_: float):
    return np.sqrt(4/(np.pi * tau_ * 9 * D)) * delta_V_s

def delta_V_t_sim(D_p: float, D_n: float, tau_, delta_V_tp, delta_V_tn):
    return delta_V_ti(D=D_p, delta_V_s=delta_V_tp, tau_=tau_) + delta_V_ti(D=D_n, delta_V_s=delta_V_tn, tau_=tau_)


def func_obj(lst_param: list):
    D_p, D_n = lst_param[0], lst_param[1]
    df_exp = pd.read_csv('GITT_25.csv')
    SOC_prev = 0.9
    mse_sum = 0
    for cycle_index in range(2, 10):
        SOC = 1 - cycle_index * 0.1
        tau_ = tau(df_exp=df_exp, cycle_index=cycle_index)
        delta_V_t_exp_ = delta_V_t_exp(df_exp=df_exp, cycle_index=cycle_index)
        delta_V_s_ = delta_V_s(df_exp=df_exp, cycle_index=cycle_index)
        cap_ = cap(df_exp=df_exp, cycle_index=cycle_index)
        OCP_p_prev, OCP_n_prev, OCV_prev = OCV(SOC_LIB=SOC_prev,
                                               SOC_n_min=0.01073305, SOC_n_max=0.82852023,
                                               SOC_p_min=0.41553058, SOC_p_max=0.90207103)
        OCP_p, OCP_n, OCV_ = OCV(SOC_LIB=SOC,
                                SOC_n_min=0.01073305, SOC_n_max=0.82852023,
                                SOC_p_min=0.41553058, SOC_p_max=0.90207103)
        delta_OCP_n = OCP_p_prev - OCP_p
        delta_OCP_p = OCP_n_prev - OCP_n
        SOC_prev = SOC
        delta_V_t_sim_ = delta_V_t_sim(D_p=D_p, D_n=D_n, tau_=tau_, delta_V_tp=delta_OCP_p, delta_V_tn=delta_OCP_n)
        mse_sum += (delta_V_t_sim_ - delta_V_t_exp_)**2
    return mse_sum

obj_ga = GA(n_chromosomes=100, bounds=np.array([[1e-4, 1.6e-3], [4.4e-5, 3.9e-4]]), obj_func=func_obj,
            n_pool=7, n_elite=3,
            n_generations=100)
array_param,_ = obj_ga.solve()

# df_exp = df_exp[(df_exp['Cycle_Index'] == 3) & (df_exp['Step_Index'] == 6)]
# # print(df_exp['Step_Index'].unique())
# t_exp = df_exp['t [s]']
# I_exp = df_exp['I [A]']
# V_exp = df_exp['V [V]']
# cap_charge = df_exp['cap_charge [Ahr]']
# cap_discharge = df_exp['cap_discharge [Ahr]']
#
# # Plots
# fig = plt.figure()
# ax1 = fig.add_subplot(211)
# ax1.plot(t_exp, V_exp)
#
# ax2 = fig.add_subplot(212)
# ax2.plot(t_exp, I_exp)
#
# plt.show()
