import SPPy

import matplotlib.pyplot as plt


# Operating parameters
I = 1.92
T = 298.15
V_max = 4.2
SOC_min = 0.1
SOC_LIB = 1

# Modelling parameters
SOC_init_p, SOC_init_n = 0.9979522597286746, 0.01054526104056893

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell.cap = 1.92

# set-up cycler and solver
dc = SPPy.Charge(charge_current=I, V_max=V_max, SOC_max=1, SOC_LIB=0)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')

# simulate
sol = solver.solve(cycler_instance=dc)

print(sol.x_surf_p[-1])
print(sol.x_surf_n[-1])

# Plot
fig = plt.figure(figsize=(7.5, 3), dpi=300)

ax1 = fig.add_subplot(121)
ax1.plot(sol.t, sol.V, label = "Cell Terminal Voltage [V]", linewidth=3)
ax1.plot(sol.t, sol.OCV_LIB, label="Open-Circuit Potential [V]", linewidth=3)
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Potential [V]')
ax1.legend()

ax2 = fig.add_subplot(122)
ax2.plot(sol.t, sol.V - sol.OCV_LIB, )
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Potential [V]')

plt.tight_layout()
plt.savefig('G:\My Drive\Writings\Electrochemical_models\SPM\overpotential_charge.png')
plt.show()
