import numpy as np

from SPPy.calc_helpers.constants import Constants


def OCP_ref_p(x):
    # function calculations
    A_list = [5166082.0, -5191279.0, 5232986.0, -5257083.0, 5010583.0, -4520614.0, 7306952.0, -14634260.0, 6705611.0,
              33894160.0, -63528110.0, 30487930.0, 21440020.0, -27731990.0, 8206452.0]
    K = -2.369020e-04
    R = Constants.R
    F = Constants.F
    T = 298.15
    # second term
    sec_term = (R*T / F) * np.log((1-x)/x)
    # third term
    pre_term = 1/(K * (2*x-1) + 1)**2
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A/F) * ((2*x-1)**(i+1) - 2*i*x*(1-x) / (2*x-1)**(1-i))
    third_term = pre_term * post_term
    # fourth term
    post_term = 0
    for i, A in enumerate(A_list):
        post_term += (A/F) * ((2*x-1) ** i) * (2*(i+1)*(x**2) - 2*(i+1)*x + 1)
    fou_term = K * post_term
    return -2.276828e+01 + sec_term + third_term + fou_term