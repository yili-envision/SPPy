import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate

from parameter_sets.Calce_NMC_18650.funcs import OCP_ref_p



df = pd.read_csv('../../../../general_OCP/NMC_lith_schmitt_et_al.csv')
SOC = df['SOC'].to_numpy() * (0.98-0.4) + 0.4  # TODO: fix the mixup in the csv file
OCP = df['OCP [V]'].to_numpy()  # TODO: fix the mixup in the csv file

func_OCP_ref_p = scipy.interpolate.interp1d(SOC, OCP)

array_SOC_guo = np.linspace(0.4, 1)
array_SOC_schmitt = np.linspace(0.401, 0.979)
array_OCP_guo = OCP_ref_p(array_SOC_guo)
array_OCP_schmitt = func_OCP_ref_p(array_SOC_schmitt)

plt.plot(array_SOC_guo, array_OCP_guo)
plt.plot(array_SOC_schmitt, array_OCP_schmitt)
plt.show()
