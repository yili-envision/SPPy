import numpy as np
import matplotlib.pyplot as plt

from SPPy.solvers.electrolyte_conc import ElectrolyteFVMCoordinates, ElectrolyteConcFVMSolver
from SPPy.models.battery import SPMe


co_ords = ElectrolyteFVMCoordinates(D_e=7.5e-10, epsilon_en=0.385, epsilon_esep=0.785, epsilon_ep=0.485,
                                    L_n=8e-5, L_s=2.5e-5, L_p=8.8e-5, brugg=4)
conc_solver = ElectrolyteConcFVMSolver(co_ords=co_ords, transference=0.354)

j_p = SPMe.molar_flux_electrode(I=-1.656, S=1.1167, electrode_type='p') * np.ones(len(co_ords.array_x_p))
j_sep = np.zeros(len(co_ords.array_x_s))
j_n = SPMe.molar_flux_electrode(I=-1.656, S=0.7824, electrode_type='n') * np.ones(len(co_ords.array_x_n))
j = np.append(np.append(j_n, j_sep), j_p)

a_sn = 5.78e03 * np.ones(len(co_ords.array_x_n))
a_sep = np.zeros(len(co_ords.array_x_s))
a_sp = 7.28e03 * np.ones(len(co_ords.array_x_p))
a_s = np.append(np.append(a_sn, a_sep), a_sp)

c_prev = 1000 * np.ones(len(co_ords.array_x))
dt = 0.1

for i in range(3600):
    c_e = conc_solver.solve_ce(c_prev=c_prev, j=j, dt=dt, a_s=a_s, solver_method='TDMA')
    c_prev = c_e

print(c_e)
plt.plot(co_ords.array_x, c_e)
plt.show()