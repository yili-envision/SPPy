import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from analysis.cycling.CalcePL.PL4.exp_cap import cap as cap_PL4
from analysis.cycling.CalcePL.PL21.exp_cap import cap as cap_PL21
from analysis.cycling.CalcePL.PL11.exp_cap import cap as cap_PL11


# exp data
cycle_full_array = np.arange(0, 800, 50)
cap_exp_list_PL4 = cap_PL4(cycle_no=cycle_full_array)
cap_exp_list_PL21 = cap_PL21(cycle_no=cycle_full_array)
cap_exp_list_PL11 = cap_PL11(cycle_no=cycle_full_array)

# sim data
cycle_no_4060 = pd.read_csv('PL4/cycling_sim_data.csv')['Cycle_no'].to_numpy()
NDC_4060 = pd.read_csv('PL4/cycling_sim_data.csv')['NDC'].to_numpy()
cycle_no_2080 = pd.read_csv('PL21/cycling_sim_data.csv')['Cycle_no'].to_numpy()
NDC_2080 = pd.read_csv('PL21/cycling_sim_data.csv')['NDC'].to_numpy()
cycle_no_0100 = pd.read_csv('PL11/cycling_sim_data.csv')['Cycle_no'].to_numpy()
NDC_0100 = pd.read_csv('PL11/cycling_sim_data.csv')['NDC'].to_numpy()

# Plots
#       Plot settings
mpl.rcParams['lines.linewidth'] = 3
plt.rc('axes', titlesize=15)
plt.rc('axes', labelsize=15)
#      Plots for 40-60
plt.plot(cycle_no_4060, NDC_4060, label="sim (40%-60%)")
plt.scatter(cycle_full_array, cap_exp_list_PL4/100, label="exp (40%-60%)")
#       Plots for 20-80
plt.plot(cycle_no_2080, NDC_2080, label="sim (20%-80%)")
plt.scatter(cycle_full_array, cap_exp_list_PL21/100, label="exp (20%-80%)")
#       # Plots for 0-100
# plt.plot(cycle_no_0100, NDC_0100, label="sim (0%-100%)")
# plt.scatter(cycle_full_array, cap_exp_list_PL11/100, label="exp (0%-100%)")

plt.xlabel('Cycle No.')
plt.ylabel('Normalized Discharge Capacity')
plt.title('NDC vs. cycle')
plt.ylim(0.85, 1.01)
plt.legend()
plt.show()