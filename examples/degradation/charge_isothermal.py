import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_max = 4.2
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.989011, 0.01890232

# Setup battery components
cell1 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)


# set-up cycler and solver
cc = SPPy.Charge(charge_current=I, V_max=V_max)
solver1 = SPPy.SPPySolver(b_cell=cell1, N=5, isothermal=True, degradation=True)

# simulate
sol1 = solver1.solve(cycler_instance=cc)

# Plot
sol1.plot_SEI()
