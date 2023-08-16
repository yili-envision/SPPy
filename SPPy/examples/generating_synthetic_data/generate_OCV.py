import SPPy

import matplotlib.pyplot as plt


# Operating parameters
I = 1.92
T = 298.15
V_min = 2.5
SOC_min = 0.1
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell.cap = 1.92

# set-up cycler and solver
# dc = SPPy.DischargeRest(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
dc = SPPy.DischargeRest(discharge_current=I, V_min=V_min, SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_min, SOC_LIB_max=1,
                        rest_time=3600)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

print(sol.x_surf_p[-1])
print(sol.x_surf_n[-1])

# Plot
# sol.comprehensive_plot()
plt.plot(sol.t, sol.V)
plt.plot(sol.t, sol.OCV_LIB)
# plt.plot(sol.t, sol.x_surf_p)
# plt.plot(sol.t, sol.x_surf_n)
plt.show()