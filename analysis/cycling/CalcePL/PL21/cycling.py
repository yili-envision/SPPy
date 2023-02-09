import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from file_path_variables import *
from data.Calce_PL import funcs
from data.general_OCP.LCO import OCP_ref_p
from src.battery_components.battery_cell import BatteryCell
from src.models.single_particle_model import SPModel
from src.solvers.eigen_func_exp import EigenFuncExp
from src.models.degradation import ROM_SEI
from src.cycler.cc import CC,CCNoFirstRest

from exp_cap import cap


# Operating parameters
T = 298.15
V_min_full = 3
V_max_full = 4.2
V_min_partial = 2
V_max_partial = 4.5
num_cycles_partial = 50
num_cycles_full = 1
charge_current = 0.75
discharge_current = 0.75
rest_time = 1795

# Modelling parameters
t_increment = 1
# # SOC_init_p, SOC_init_n = 0.9030092608479767, 0.13857156903558143 # ga results for V-terminated
# SOC_init_p, SOC_init_n = 0.852422478611043, 0.20973244470098207 # ga results for SOC-terminated
SOC_init_p, SOC_init_n = 0.852422478611043, 0.085

# Setup battery components and model with the results from genetic algorithm
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=OCP_ref_p,
                   func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                   func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                   filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
cell.elec_p.max_conc, cell.elec_n.max_conc = 47000, 25000 # manual
cell.R_cell = 0.06230465601788312
model = SPModel(isothermal=False, degradation=True)
SEI_model = ROM_SEI(bCell= cell, file_path= SEI_DIR, resistance_init=1e-8, thickness_init=0)
SEI_model.i_0s = 1e4

# set-up cycler and solver
cycle_full_list = []
cap_sim_list = []
cycle_full_ = 1

cycler_full = CC(num_cycles=num_cycles_full, charge_current=charge_current, discharge_current=discharge_current,
                 rest_time=rest_time, V_max=V_max_full, V_min=V_min_full)
# cycler_full = cycler = CCNoFirstRest(num_cycles=num_cycles_full, charge_current=charge_current, discharge_current=discharge_current,
#                        rest_time=rest_time, V_max=V_max_full, V_min=V_min_full, SOC_min=0, SOC_max=1, SOC_LIB=0.2)
cycler_inter = cycler = CCNoFirstRest(num_cycles=2, charge_current=charge_current, discharge_current=discharge_current,
                       rest_time=rest_time, V_max=V_max_full, V_min=V_min_full, SOC_min=0.2, SOC_max=0.8, SOC_LIB=0)
cycler_partial = cycler = CCNoFirstRest(num_cycles=num_cycles_partial, charge_current=charge_current, discharge_current=discharge_current,
                       rest_time=rest_time, V_max=V_max_partial, V_min=V_min_partial, SOC_min=0.2, SOC_max=0.8, SOC_LIB=0.2)
solver = EigenFuncExp(b_cell=cell, b_model=model, N=5, SEI_model=SEI_model)

for i in range(16):

    # full cycle
    cycle_full_list.append(cycle_full_)
    sol_full = solver.solve(cycler=cycler_full, verbose=False, t_increment=t_increment, termination_criteria = 'V')
    # calc capacity from full cycle
    cap_sim = sol_full.dis_cap_array()
    cap_sim_list.append(cap_sim)

    # list to numpy array
    cycle_full_array = np.array(cycle_full_list)
    cap_sim_array = np.array(cap_sim_list)
    cap_exp = cap_sim_array[0] * cap(cycle_full_array) / 100

    # # save data
    if i > 0:
        df = pd.DataFrame({'cycle_no': cycle_full_list,'cap_sim [Ahr]': cap_sim_list})
        df.to_csv('cycling_sim.csv', index=0)

    # # plots
    # sol_full.comprehensive_plot()
    plt.scatter(cycle_full_array, cap_exp, label="exp")
    plt.scatter(cycle_full_array, cap_sim_list, label="sim")
    plt.legend()
    plt.show()

    # Charge a using intermediate cycling condition
    sol_inter = solver.solve(cycler=cycler_inter, verbose=False, t_increment=t_increment, termination_criteria='SOC')

    #      Solve for partial cycles
    sol_partial = solver.solve(cycler=cycler_partial, verbose=False, t_increment=t_increment, termination_criteria = 'SOC')
    # update cycle number
    cycle_full_ += num_cycles_partial
    # print the SEI thickness
    print('cycle:', cycle_full_, 'SEI_thickness: ', SEI_model.thickness)

    # sol_partial.comprehensive_plot()