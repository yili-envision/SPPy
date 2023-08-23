import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs
from parameter_sets.test.funcs import OCP_ref_n


electrode_temp = 298.15
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al


SOC_PC = np.linspace(1e-12, 0.69)
OCP_PC = funcs.extract_OCP(SOC_PC, specie_name='Petroleum_coke', T=electrode_temp)

SOC_graphite = np.linspace(0, 0.815)
OCP_graphite = OCP_ref_n(SOC_graphite)

print(OCP_graphite[-1])

# Plots
plt.plot(SOC_PC, OCP_PC, label="Petroleum Coke")
plt.plot(SOC_graphite, OCP_graphite, label="graphite")

plt.grid()
plt.legend()
plt.show()