import numpy as np
import pandas as pd

from SPPy.sol_and_visualization.solution import Solution


df_exp = pd.read_csv('../../../../data/Calce_OCV/OCV.csv')
cell_cap = 2.15
# The experiment consists of
# rest (step=2)
# discharge (step=3),
# rest (step=4, rest time = 7200s),
# charge cycles(step=5)
# final rest (step=6, rest time = 7200s)

# t_exp = df_exp['t [s]'].to_numpy()
# I_exp = df_exp['I [mA]'].to_numpy() / 1000
# V_exp = df_exp['V [mV]'].to_numpy() / 1000

# df_exp_rest = df_exp[df_exp['step'] == 2]
# t_exp_rest = df_exp_rest['t [s]'].to_numpy() - df_exp_rest['t [s]'].iloc[0]
# I_exp_rest = df_exp_rest['I [mA]'].to_numpy() / 1000
# V_exp_rest = df_exp_rest['V [mV]'].to_numpy() / 1000

# df_exp_discharge = df_exp[df_exp['step'] == 3]
# t_exp_discharge = df_exp_discharge['t [s]'].to_numpy() - df_exp_discharge['t [s]'].iloc[0]
# I_exp_discharge = df_exp_discharge['I [mA]'].to_numpy() / 1000
# V_exp_discharge = df_exp_discharge['V [mV]'].to_numpy() / 1000
# dt_exp_discharge = np.diff(t_exp_discharge, prepend=0)
# dcap_exp_discharge = dt_exp_discharge * I_exp_discharge / (3600 * cell_cap)
# cap_exp_discharge = 1 + np.cumsum(dcap_exp_discharge)

sol_exp = Solution.upload_exp_data(file_name='../../../../data/Calce_OCV/OCV.csv', step_num=3)

dt_exp_discharge = np.diff(sol_exp.t, prepend=0)
dcap_exp_discharge = dt_exp_discharge * sol_exp.I / (3600 * cell_cap)
sol_exp.cap_discharge = 1 + np.cumsum(dcap_exp_discharge)


# df_exp_dischargerest = df_exp[(df_exp['step'] == 3) | (df_exp['step'] == 4)]
# t_exp_dischargerest = df_exp_dischargerest['t [s]'].to_numpy() - df_exp_discharge['t [s]'].iloc[0]
# I_exp_dischargerest = df_exp_dischargerest['I [mA]'].to_numpy() / 1000
# V_exp_dischargerest = df_exp_dischargerest['V [mV]'].to_numpy() / 1000
#
# df_exp_dischargerestcharge = df_exp[(df_exp['step'] == 3) | (df_exp['step'] == 4) | (df_exp['step'] == 5)]
# t_exp_dischargerestcharge = df_exp_dischargerestcharge['t [s]'].to_numpy() - df_exp_discharge['t [s]'].iloc[0]
# I_exp_dischargerestcharge = df_exp_dischargerestcharge['I [mA]'].to_numpy() / 1000
# V_exp_dischargerestcharge = df_exp_dischargerestcharge['V [mV]'].to_numpy() / 1000
#
# df_exp_dischargerestchargerest = df_exp[(df_exp['step'] == 3) | (df_exp['step'] == 4) | (df_exp['step'] == 5)
#                                         | (df_exp['step'] == 6)]
# t_exp_dischargerestchargerest = df_exp_dischargerestchargerest['t [s]'].to_numpy() - df_exp_discharge['t [s]'].iloc[0]
# I_exp_dischargerestchargerest = df_exp_dischargerestchargerest['I [mA]'].to_numpy() / 1000
# V_exp_dischargerestchargerest = df_exp_dischargerestchargerest['V [mV]'].to_numpy() / 1000
#
# # Display important results
# print('OCV at fully charged [V]', V_exp_rest.mean())
# print('rest time after discharge [s]', t_exp_dischargerest[-1] - t_exp_discharge[-1])
# print('Charge current [A]', df_exp[df_exp['step'] == 5]['I [mA]'].to_numpy().mean() / 1000)
# print('rest time after discharge [s]', df_exp[df_exp['step'] == 6]['t [s]'].to_numpy()[-1] - \
#       df_exp[df_exp['step'] == 6]['t [s]'].to_numpy()[0])


# # # Plots
# plt.plot(t_exp_dischargerestchargerest, V_exp_dischargerestchargerest)
# plt.show()


