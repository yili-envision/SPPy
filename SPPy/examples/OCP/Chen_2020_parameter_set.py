import numpy as np
import matplotlib.pyplot as plt

from parameter_sets.Chen_2020 import funcs


SOC_n = np.linspace(0, 1)
OCP_n = funcs.OCP_ref_n(SOC_n)

plt.plot(SOC_n, OCP_n, label='n')
plt.xlabel('SOC_n')
plt.ylabel('OCP [V]')

plt.legend()
plt.show()
