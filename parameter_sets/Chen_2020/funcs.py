import numpy as np


def OCP_ref_n(SOC):
    return 1.9793 * np.exp(-39.3631) + \
           0.2482 - \
           0.0909 * np.tanh(29.8538 * SOC - 0.1234) - \
           0.04478 * np.tanh(14.9159 * SOC - 0.2769) - \
           0.0205 * np.tanh(30.4444 * SOC - 0.6103)