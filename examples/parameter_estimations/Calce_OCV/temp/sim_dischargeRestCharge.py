import SPPy


# Operating parameters
discharge_current = charge_current = 0.1
T = 298.15  # in K
V_min = 2.5  # in V
V_max = 4.15  # in V
SOC_min = 0
SOC_LIB = 1
SOC_LIB_max = 1
rest_time = 7200  # in s

# Modelling parameters
SOC_init_p, SOC_init_n = 0.43736824, 0.8136202  # from GA results


# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='Calce_OCV', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# set-up cycler and solver
dc = SPPy.DischargeRestCharge(discharge_current=discharge_current, charge_current=charge_current, rest_time=rest_time,
                              V_min=V_min, V_max=V_max,
                              SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB, SOC_LIB_max=SOC_LIB_max)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate and save
sol = solver.solve(cycler_instance=dc, verbose='True', t_increment=1)
sol.save_instance('sol_dischargeRestCharge')

print(sol.t)

# Plot
# sol.comprehensive_plot()