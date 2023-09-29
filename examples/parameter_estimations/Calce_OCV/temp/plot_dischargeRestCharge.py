import pickle

from extract_exp_data import *
import scipy.interpolate


with open("sol_fullOCV", "rb") as file:
    sol = pickle.load(file)

# def V_sim_extrapolate():
#     return scipy.interpolate.interp1d(sol.t, sol.V)

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax1.plot(sol.t, sol.V, label='sim')
ax1.plot(t_exp_dischargerestchargerest, V_exp_dischargerestchargerest, label="exp")
ax1.legend()

# ax2 = fig.add_subplot(222)
# ax2.plot(t_exp_discharge[1000:-1000], V_sim_extrapolate()(t_exp_discharge[1000:-1000]) - V_exp_discharge[1000:-1000])

ax3 = fig.add_subplot(223)
ax3.plot(sol.t, sol.x_surf_p)

ax4 = fig.add_subplot(224)
ax4.plot(sol.t, sol.x_surf_n)

plt.legend()
plt.tight_layout()
plt.show()
