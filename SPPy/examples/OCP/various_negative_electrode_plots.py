import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs


electrode_temp = 298.15
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al


SOC_n = np.linspace(0, 0.75)
OCP_NCA = funcs.extract_OCP(SOC_n, specie_name='Petroleum_coke', T=electrode_temp)


plt.plot(SOC_n, OCP_NCA)

plt.show()