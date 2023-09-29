import pickle

import matplotlib.pyplot as plt

import SPPy
from extract_exp_data import *
import scipy.interpolate


with open("sol_discharge", "rb") as file:
    sol = pickle.load(file)

def V_sim_extrapolate():
    return scipy.interpolate.interp1d(sol.t, sol.V)

# SPPy.Plots(sol, sol_exp).comprehensive_plot()

fig = plt.figure()

ax1 = fig.add_subplot(221)
ax1.plot(sol.t, sol.V, label="sim")
ax1.plot(sol_exp.t, sol_exp.V, label="exp")
ax1.legend()

ax2 = fig.add_subplot(222)
ax2.plot(sol.SOC_LIB, sol.OCV_LIB, label="sim")
ax2.plot(sol_exp.cap, sol_exp.V, label="exp")
ax2.legend()

# ax2 = fig.add_subplot(222)
# ax2.plot(t_exp_discharge[1000:-1000], V_sim_extrapolate()(t_exp_discharge[1000:-1000]) - V_exp_discharge[1000:-1000])

ax3 = fig.add_subplot(223)
ax3.plot(sol.t, sol.x_surf_p)
#
ax4 = fig.add_subplot(224)
ax4.plot(sol.t, sol.x_surf_n)

print(sol.x_surf_n[-1])
print(sol.x_surf_p[-1])
print(sol.OCV_LIB[-1])
print(sol_exp.t[-1])

plt.legend()
plt.tight_layout()
plt.show()
