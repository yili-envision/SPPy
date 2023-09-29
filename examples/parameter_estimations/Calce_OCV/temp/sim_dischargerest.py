from extract_exp_data import *

import SPPy


# Operating parameters
I = 0.1
T = 298.15
V_min = 2.5
SOC_min = 0
SOC_max=1
SOC_LIB = 1
rest_time = 7200

# Modelling parameters
SOC_init_p, SOC_init_n = 0.43736824, 0.8136202  # from GA results


# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# set-up cycler and solver
dc = SPPy.DischargeRest(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB, rest_time=rest_time,
                        SOC_LIB_max=SOC_min)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate and save
sol = solver.solve(cycler_instance=dc, verbose='True', t_increment=1)
sol.save_instance('sol_dischargerest')

# Plot
# sol.comprehensive_plot()