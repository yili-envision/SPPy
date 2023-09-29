import numpy as np

from extract_exp_data import *
from parameter_sets.Calce_NMC_18650.funcs import OCP_ref_n, OCP_ref_p

from SPPy.calc_helpers.optimizations import GA
from OCP import OCV, func_OCV_exp, mse


def func_obj(lst_param):
    array_SOC_LIB = np.linspace(1e-5, 1)
    _,_,array_OCV_sim = OCV(SOC_LIB=array_SOC_LIB, SOC_n_min=lst_param[0], SOC_n_max=lst_param[1],
                        SOC_p_min=lst_param[2], SOC_p_max=lst_param[3])
    array_OCV_exp = func_OCV_exp(array_SOC_LIB)
    mse_all = mse(array_exp=array_OCV_exp, array_sim=array_OCV_sim)
    mse_l = mse(array_OCV_exp[np.argwhere(array_SOC_LIB < 0.1)], array_OCV_sim[np.argwhere(array_SOC_LIB < 0.1)])
    return 0.5 * mse_all + 0.5 * mse_l


obj_ga = GA(n_chromosomes=1000, bounds=np.array([[0, 0.05], [0.62, 0.805], [0.36, 0.5], [0.9, 1]]), obj_func=func_obj,
            n_pool=7, n_elite=3,
            n_generations=100)
array_param,_ = obj_ga.solve()

# print(array_param, OCV(array_chromosome=array_param))