import numpy as np

from src.calc_helpers.constants import Constants


def OCP_ref_n(x):
    A_list = [643.3323, 92777.34, 120803.9, 39097.09, 70427.33, 452782.1, 925998.1, 111.1642, -1853447.0, -323266.3,
              3899277.0, 2862780.0, -2837527.0, -4199996.0, -1406372.0]
    K = 9.896854e-01
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
    return 5.839445e-01 + sec_term + third_term + fou_term