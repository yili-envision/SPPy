import numpy as np
from SPPy.general_OCP import funcs


def OCP_ref_p(SOC):
    return funcs.extract_OCP(SOC, specie_name='NMC', T=298.15)


def dOCPdT_p(SOC):
    num = -0.19952 + 0.92837*SOC - 1.36455 * SOC ** 2 + 0.61154 * SOC ** 3
    dem = 1 - 5.66148 * SOC + 11.47636 * SOC**2 - 9.82431 * SOC**3 + 3.04876 * SOC**4
    return (num/dem) * 1e-3 # since the original unit are of mV/K


def OCP_ref_n(SOC):
    return 0.13966 + 0.68920 * np.exp(-49.20361 * SOC) + 0.41903 * np.exp(-254.40067 * SOC) \
            - np.exp(49.97886 * SOC - 43.37888) - 0.028221 * np.arctan(22.52300 * SOC - 3.65328) \
            -0.01308 * np.arctan(28.34801* SOC - 13.43960)


def dOCPdT_n(SOC):
    num = 0.00527 + 3.29927 * SOC - 91.79326 * SOC ** 2 + 1004.91101 * SOC ** 3 - \
          5812.27813 * SOC ** 4 + 19329.75490 * SOC ** 5 - 37147.89470 * SOC ** 6 + \
          38379.18127 * SOC ** 7 - 16515.05308 * SOC ** 8
    dem = 1 - 48.09287 * SOC + 1017.23480 * SOC**2 - 10481.80419 * SOC**3 + \
          59431.30001 * SOC**4 - 195881.64880 * SOC**5 + 374577.31520 * SOC**6 - \
          385821.16070 * SOC**7 + 165705.85970 * SOC**8
    return (num/dem) * 1e-3 # since the original unit are of mV/K

