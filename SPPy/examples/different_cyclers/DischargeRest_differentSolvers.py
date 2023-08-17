import SPPy

import matplotlib.pyplot as plt


# Operating parameters
I = 1.65
T = 298.15
V_min = 2.5
SOC_min = 0.1
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell1 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell2 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell3 = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)


# set-up cycler and solver
dc = SPPy.DischargeRest(discharge_current=I, V_min=V_min, SOC_LIB=SOC_LIB, SOC_LIB_min=SOC_min, SOC_LIB_max=1,
                        rest_time=3600)
solver_poly = SPPy.SPPySolver(b_cell=cell1, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')
solver_eigen = SPPy.SPPySolver(b_cell=cell2, N=5, isothermal=True, degradation=False, electrode_SOC_solver='eigen')
solver_cn = SPPy.SPPySolver(b_cell=cell3, N=5, isothermal=True, degradation=False, electrode_SOC_solver='cn')


# simulate
sol_poly = solver_poly.solve(cycler_instance=dc)
dc.reset_time_elapsed()
sol_eigen = solver_eigen.solve(cycler_instance=dc)
dc.reset_time_elapsed()
sol_cn = solver_cn.solve(cycler_instance=dc)

# Plot
fig = plt.figure(figsize=(4,3), dpi=300)
ax1 = fig.add_subplot(111)
ax1.plot(sol_poly.t, sol_poly.V, label="Polynomial Approximation", linewidth=2)
ax1.plot(sol_eigen.t, sol_eigen.V, label="Eigen Expansion Method", linewidth=2)
ax1.plot(sol_cn.t, sol_cn.V, label="Crank-Nicolson Scheme", linewidth=2)
plt.arrow(x=4300, y=3.7, dx=0, dy=0.01, width=.08)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Cell Terminal Voltage [V]')
# ax1.legend()

plt.tight_layout()
plt.savefig('G:\My Drive\Writings\Electrochemical_models\SPM\DischargeRest_differentSolvers.png')
plt.show()
