import pandas as pd
import numpy as np

from SPPy.calc_helpers.constants import Constants


def extract_OCP(x, specie_name, T):
    # function calculations
    df = pd.read_csv('../../../data/general_OCP/coefficents.csv', index_col=0)[specie_name]
    A_list = [df[index_name] for index_name in df.index if index_name[0] == 'A']
    K = df['K']
    R = Constants.R
    F = Constants.F
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
    return df['U0'] + sec_term + third_term + fou_term