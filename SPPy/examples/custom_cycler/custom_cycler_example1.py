import pandas as pd
import matplotlib.pyplot as plt

import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4
num_cycles = 10
charge_current = 1.656
discharge_current = 1.656
rest_time = 30

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

# set-up cycler and solver. Also plot the cycler time [s] and current [A]. For this example the data is extracted from
# a csv file.
df = pd.read_csv('example_data.csv')
cycler = SPPy.CustomCycler(t_array=df['t [s]'].to_numpy(), I_array=df['I [A]'].to_numpy(), SOC_LIB=1.0)
cycler.plot()
solver = SPPy.SPPySolver(b_cell= cell, N=5, isothermal=True, degradation=False)

# simulate and plot
sol = solver.simple_solve(custom_cycler_instance=cycler, verbose=False)

plt.plot(sol.t, sol.V)
plt.show()