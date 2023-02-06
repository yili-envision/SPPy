import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate


from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from data.general_OCP.hard_carbon import OCP_ref_n
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.eigen_func_exp import EigenFuncExp
from src.cycler.discharge import Discharge, DischargeRest

from src.calc_helpers.genetic_algorithm import ga


# function to correct time in exp data
def correct_time(x, t_init):
    return x - t_init

# Calce data
df_exp = pd.read_csv("C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/FirstDischarge.csv")
df_exp = df_exp[df_exp['Time_sec'] > 60]
# df_exp = df_exp[(df_exp['Current_Amp'] != 0)]
# t_init = df_exp['Time_sec'].iloc[0]
# df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = -df_exp['Current_Amp'].to_numpy()

def sim(SOC_init_p, SOC_init_n, R_cell, max_conc_n, R_n):
    # Operating parameters
    T = 298.15
    V_min = 2.8
    discharge_current = 0.75
    rest_time = 3600

    # Setup battery components
    cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                       func_dOCPdT_p=funcs.dOCPdT_p, filepath_n=TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                       func_OCP_n=OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                       filepath_electrolyte=TEST_ELECTROLYTE_DIR, filepath_cell=TEST_BATTERY_CELL_DIR, T=T)
    cell.R_cell = R_cell
    cell.elec_n.max_conc = max_conc_n
    cell.elec_n.R = R_n
    model = SPModel(isothermal=False, degradation=False)

    # set-up solver and solve
    cycler = DischargeRest(discharge_current=discharge_current, rest_time=rest_time, V_min=V_min)
    solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
    sol = solver.solve(cycler=cycler, verbose=False, t_increment=1)
    return sol.t, sol.V


def func_sim(SOC_init_p, SOC_init_n, R_cell, max_conc_n, R_n, t_exp, V_exp):
    t, V = sim(SOC_init_p, SOC_init_n, R_cell, max_conc_n, R_n)
    try:
        tV_func_sim = interpolate.interp1d(t, V)
        V_sim = tV_func_sim(t_exp)
        # calc mse
        mse = np.mean(np.square(V_exp - V_sim))
    except:
        # # if t is shorter than t_exp add more elements to the V array
        # V_sim_extra = V[-1] * np.ones(7200)
        # V = np.append(V, V_sim_extra)
        # tV_func_sim = interpolate.interp1d(t, V)
        # V_sim = tV_func_sim(t_exp)
        # # calc mse
        # mse = np.mean(np.square(V_exp - V_sim))
        mse = 1000
    return mse


# define objective func for genetic_algorithm
def objective_func(row):
    """
    objective func for GA
    :param row:
    row[0]: SOC_p_init
    row[1]: SOC_n_init
    row[2]: R_cell
    row[3]: max_conc_n
    row[4]: R_n
    :return:
    """
    mse = func_sim(row[0], row[1], row[2], row[3], row[4], t_exp=t_exp, V_exp=V_exp)
    print(mse)
    return mse

# perform genetic algorithm
df_GA_results,param, fitness = ga(objective_func, n_generation=5,
                                  n_chromosones= 100, n_genes=5,
                                  bounds = [[0.35, 0.6],
                                            [0.6, 0.8],
                                            [0.15, 0.4],
                                            [25000, 60000],
                                            [1e-5, 2e-5]],
                                  n_pool = 3,
                                  n_elite=1,
                                  c_f = 0.8)

# print params
param_dict = {'SOC_p_init': param[0],'SOC_n_init': param[1],'R_cell': param[2],'max_conc_n': param[3],'R_n': param[4]}
print(param_dict)

# perform simulation on the best found parameters
t_sim, V_sim = sim(param[0], param[1], param[2], param[3], param[4])

# Plot
plt.plot(t_exp, V_exp, label="exp")
plt.plot(t_sim, V_sim, label="sim")
plt.legend()
plt.show()