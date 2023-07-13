import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs


electrode_temp = 298.15

SOC_n = np.linspace(0.15, 1)
OCP_NCA = funcs.extract_OCP(SOC_n, specie_name='NCA', T=electrode_temp)

plt.plot(SOC_n, OCP_NCA)
plt.show()