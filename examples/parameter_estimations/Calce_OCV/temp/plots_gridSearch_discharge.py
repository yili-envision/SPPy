import numpy as np

from SPPy.parameter_estimations.rough_estimations import GridSearch

from extract_exp_data import *

array_sol_num = np.arange(813, 831, 1)
array_sol_close1 = np.array([706, 707, 712, 713, 714, 800])
array_sol_close = np.array([707, 815])
GridSearch.plot_generated_data(lst_sol_num=array_sol_close,
                               t_exp=t_exp_discharge, V_exp=V_exp_discharge,
                               show_legends=True)



