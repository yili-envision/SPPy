import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.SPPySolver(b_cell= cell, N=5, isothermal=True, degradation=False)

# simulate
sol = solver.solve(cycler=dc)

print(sol.cycle_summary)

# Plot
sol.comprehensive_plot()
