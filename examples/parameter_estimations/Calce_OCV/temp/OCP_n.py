import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.interpolate

from parameter_sets.Calce_NMC_18650.funcs import OCP_ref_n



df = pd.read_csv('../../../../general_OCP/schmitt_et_al.csv')
OCP = df['SOC'].to_numpy()  # TODO: fix the mixup in the csv file
SOC = df['OCP [V]'].to_numpy() * (0.815-0)  # TODO: fix the mixup in the csv file

# plt.plot(OCP, SOC)
# plt.show()

func_OCP_ref_n = scipy.interpolate.interp1d(SOC, OCP)

array_SOC = np.linspace(0.02, 0.815)
array_OCP_guo = OCP_ref_n(array_SOC)
array_OCP_schmitt = func_OCP_ref_n(array_SOC)

plt.plot(array_SOC, array_OCP_guo)
plt.plot(array_SOC, array_OCP_schmitt)
plt.show()
