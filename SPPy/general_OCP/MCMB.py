import numpy as np

from SPPy.calc_helpers.constants import Constants


def OCP_ref_n(x):
    A_list = [1115.732, -114405.2, -98955.51, -84726.47, -267608.3, -476169.2, 603250.8, 1867866.0, -1698309.0,
              -5707850.0, 873999.3, 7780654.0, 1486486.0, -4703010.0, -2275145.0]
    K = 1.000052e+00
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
    return -4.894122e-01 + sec_term + third_term + fou_term