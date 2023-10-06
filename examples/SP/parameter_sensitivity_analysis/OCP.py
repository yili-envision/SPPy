import numpy as np
import matplotlib.pyplot as plt

import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

array_SOC_n = np.linspace(0, 0.8)
array_OCV_n = cell.elec_n.func_OCP(array_SOC_n)

array_SOC_p = np.linspace(0.45, 1)
array_OCV_p = cell.elec_p.func_OCP(array_SOC_p)

fig = plt.figure(figsize=(7.5, 3), dpi=300)
ax1 = fig.add_subplot(121)
ax1.plot(array_SOC_n, array_OCV_n)
ax1.set_xlabel(r'$x_n$')
ax1.set_ylabel(r'$OCP[V]$')
ax1.set_title("Negative Electrode", fontweight='bold')
ax1.arrow(x=0.75, y=0.5, dx=-0.15, dy=0, width=0.025, head_width=0.15, head_length=0.05, color='black')

ax2 = fig.add_subplot(122)
ax2.plot(array_SOC_p, array_OCV_p)
ax2.set_xlabel(r'$x_p$')
ax2.set_ylabel(r'$OCP[V]$')
ax2.set_title("Positive Electrode", fontweight='bold')
ax2.arrow(x=0.5, y=3.75, dx=0.15*0.75, dy=0, width=0.025, head_width=0.15*0.75, head_length=0.05*0.75, color='black')

plt.tight_layout()
plt.savefig('G:\My Drive\Writings\Electrochemical_models\SPM\OCP_SOC.png')
plt.show()
