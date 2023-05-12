import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import interpolate

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.cycler.cc import CCNoFirstRest
from SPPy.calc_helpers.genetic_algorithm import ga

from funcs import correct_time

# Calce data
df_exp = pd.read_csv('C:/Users/Moin/PycharmProjects/CalceData/PL/PL21/First50PartialCycles.csv')
df_exp = df_exp[df_exp['Cycle']==2]
t_init = df_exp['Time_sec'].iloc[0]
df_exp['Time_sec'] = df_exp['Time_sec'].apply(lambda x: correct_time(x, t_init=t_init))
t_exp = df_exp['Time_sec'].to_numpy()
V_exp = df_exp['Voltage_Volt'].to_numpy()
I_exp = df_exp['Current_Amp'].to_numpy()

# Operating parameters
T = 298.15
# V_min = 3.6
# V_max = 4.2
V_min = 3
V_max = 4.2
num_cycles = 1
charge_current = 0.75
discharge_current = 0.75
rest_time = 1795

def sim(SOC_init_p, SOC_init_n, R_cell, max_conc_p, max_conc_n):
    # Setup battery components
    cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                       func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                       func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                       filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
    cell.R_cell = R_cell
    cell.elec_n.max_conc = max_conc_n
    cell.elec_p.max_conc = max_conc_p
    model = SPModel(isothermal=False, degradation=False)

    # set-up solver and solve
    cycler = CCNoFirstRest(num_cycles=num_cycles, charge_current=charge_current, discharge_current=discharge_current,
                           rest_time=rest_time, V_max=V_max, V_min=V_min, SOC_min=0.2, SOC_max=0.8, SOC_LIB=0.2)
    solver = EigenFuncExp(b_cell=cell, b_model=model, N=5)
    sol = solver.solve(cycler=cycler, t_increment=1, termination_criteria = 'SOC')
    return sol.t, sol.V

def func_sim(SOC_init_p, SOC_init_n, R_cell, max_conc_p, max_conc_n, t_exp, V_exp):
    t, V = sim(SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, R_cell=R_cell, max_conc_p=max_conc_p, max_conc_n=max_conc_n)
    try:
        tV_func_sim = interpolate.interp1d(t, V)
        V_sim = tV_func_sim(t_exp[1:])
        # calc mse
        mse = np.mean(np.square(V_exp[1:] - V_sim))
    except:
        # append to t and V
        t_new = np.arange(t[-1], t[-1] + 3800, t[-1] - t[-2])
        t = np.append(t, t_new)
        V_new = V[-1] * np.ones(len(t_new))
        V = np.append(V, V_new)
        tV_func_sim = interpolate.interp1d(t, V)
        V_sim = tV_func_sim(t_exp[1:])
        # calc mse
        mse = np.mean(np.square(V_exp[1:] - V_sim))
    print('mse: ', mse)
    return mse

# define objective func for genetic_algorithm
def objective_func(row):
    """
    objective func for GA
    :param row:
    row[0]: SOC_p_init
    row[1]: SOC_n_init
    row[2]: R_cell
    row[3]: max_conc_p
    row[4]: max_conc_n
    :return:
    """
    mse = func_sim(row[0], row[1], row[2], row[3], row[4], t_exp=t_exp, V_exp=V_exp)
    print(mse)
    return mse

# perform genetic algorithm
df_GA_results,param, fitness = ga(objective_func, n_generation=5,
                                  n_chromosones= 10, n_genes=5,
                                  bounds = [[0.75, 0.99],
                                            [0.02, 0.25],
                                            [0.05, 0.1],
                                            [40000, 70000],
                                            [25000, 40000]],
                                  n_pool = 5,
                                  n_elite=1,
                                  c_f = 0.8)

# print params
param_dict = {'SOC_p_init': param[0],'SOC_n_init': param[1],'R_cell': param[2],'max_conc_p': param[3],'max_conc_n': param[4]}
print(param_dict)

# perform simulation on the best found parameters
t_sim, V_sim = sim(param[0], param[1], param[2], param[3], param[4])

# plots
plt.plot(t_exp, V_exp)
plt.plot(t_sim, V_sim)
plt.show()
