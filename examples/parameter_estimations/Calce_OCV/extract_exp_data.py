import numpy as np

import SPPy


filename = '../../../../data/Calce_OCV/OCV.csv'
cell_cap = 2.15

sol_exp = SPPy.Solution.upload_exp_data(filename=filename, step_num=3, cell_cap=cell_cap)


