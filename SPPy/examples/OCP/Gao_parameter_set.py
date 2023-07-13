import numpy as np
import matplotlib.pyplot as plt

import SPPy


electrode_temp = 298.15
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al


SOC_n = np.linspace(0, 0.8)
SOC_p = np.linspace(0.4, 1)
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=electrode_temp)


plt.plot(SOC_n, cell.elec_n.func_OCP(SOC_n), label='n')
plt.plot(SOC_p, cell.elec_p.func_OCP(SOC_p), label='p')
plt.xlabel('SOC_n')
plt.ylabel('OCP [V]')

plt.legend()
plt.show()