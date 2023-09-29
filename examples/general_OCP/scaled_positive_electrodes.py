import numpy as np
import matplotlib.pyplot as plt

from SPPy.general_OCP import funcs


electrode_temp = 298.15

array_SOC = np.linspace(0, 1)

a_min_LCO = 0.39
a_min_LFP = 0.05
a_min_LMO = 0.18
a_min_NCA = 0.19
a_min_NMC = 0.39

a_max_LCO = 1
a_max_LFP = 1
a_max_LMO = 0.95
a_max_NCA = 1
a_max_NMC = 0.99

SOC_LCO = array_SOC * (a_max_LCO - a_min_LCO) + a_min_LCO
OCP_LCO = funcs.extract_OCP(SOC_LCO, specie_name='LCO', T=electrode_temp)

SOC_LFP = array_SOC * (a_max_LFP - a_min_LFP) + a_min_LFP
OCP_LFP = funcs.extract_OCP(SOC_LFP, specie_name='LFP', T=electrode_temp)

SOC_LMO = array_SOC * (a_max_LMO - a_min_LMO) + a_min_LMO
OCP_LMO = funcs.extract_OCP(SOC_LMO, specie_name='LMO', T=electrode_temp)

SOC_NCA = array_SOC * (a_max_NCA - a_min_NCA) + a_min_NCA
OCP_NCA = funcs.extract_OCP(SOC_NCA, specie_name='NCA', T=electrode_temp)

SOC_NMC = array_SOC * (a_max_NMC - a_min_NMC) + a_min_NMC
OCP_NMC = funcs.extract_OCP(SOC_NMC, specie_name='NMC', T=electrode_temp)

plt.hlines(4.3, 0, 1, colors='red', linestyles='--')
plt.plot(array_SOC, OCP_LCO, label="LCO")
plt.plot(array_SOC, OCP_LFP, label="LFP")
plt.plot(array_SOC, OCP_LMO, label="LMO")
plt.plot(array_SOC, OCP_NCA, label="NCA")
plt.plot(array_SOC, OCP_NMC, label="NMC")

plt.legend()
plt.show()
