import numpy as np

from SPPy.parameter_estimations.rough_estimations import GridSearch

from extract_exp_data import *

# array_sol_num = np.arange(31, 36, 1)
array_sol_num = np.array([38])
GridSearch.plot_generated_data(lst_sol_num=array_sol_num,
                               t_exp=t_exp_dischargerest, V_exp=V_exp_dischargerest,
                               show_legends=True, file_dir='grid_search_results_dischargerest')