import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4.2
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.989011, 0.01890232

# Setup battery components
cell1 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell2 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)


# set-up cycler and solver
cc = SPPy.Charge(charge_current=I, V_max=V_max)
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_min=SOC_min, SOC_LIB=SOC_LIB)
solver1 = SPPy.SPPySolver(b_cell=cell1, N=5, isothermal=True, degradation=False)
solver2 = SPPy.SPPySolver(b_cell=cell2, N=5, isothermal=True, degradation=True)

# simulate
sol1 = solver1.solve(cycler=cc)
cc.reset_time_elapsed()
sol2 = solver2.solve(cycler=cc)

print(sol1.cap_charge[-1])
print(sol2.cap_charge[-1])

# Plot
SPPy.Plots(sol1, sol2).comprehensive_plot()