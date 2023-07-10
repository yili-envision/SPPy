import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4.2
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components
cell1 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell2 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell2.electrolyte.conc = 100  # changed the conc. of the electrolyte to [in mol/m3] for cell2. Cell1's
# electrolyte conc. is 1000 mol/m3


# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_min=SOC_min, SOC_LIB=SOC_LIB)
solver1 = SPPy.SPPySolver(b_cell=cell1, N=5, isothermal=True, degradation=False)
solver2 = SPPy.SPPySolver(b_cell=cell2, N=5, isothermal=True, degradation=False)

# simulate
sol1 = solver1.solve(cycler=dc, sol_name=f'c_e = {cell1.electrolyte.conc} mol/m3')
dc.reset_time_elapsed()
sol2 = solver2.solve(cycler=dc, sol_name=f'c_e = {cell2.electrolyte.conc} mol/m3')

# Plot
SPPy.Plots(sol1, sol2).comprehensive_plot()