from DischargeRest_differentSolvers import *


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