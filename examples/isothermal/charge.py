import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_max = 4.2
SOC_max = 0.9
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.989011, 0.01890232

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# set-up cycler and solver
dc = SPPy.Charge(charge_current=I, V_max=V_max, SOC_LIB_max=SOC_max, SOC_LIB=SOC_LIB)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

print(sol.cycle_summary)

# Plot
sol.comprehensive_plot()
