from file_path_variables import *
from data.test import funcs
from SPPy.battery_components.battery_cell import BatteryCell
from SPPy.models.single_particle_model import SPModel
from SPPy.solvers.eigen_func_exp import EigenFuncExp
from SPPy.cycler.cc import CC
from SPPy.models.degradation import ROM_SEI


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
V_max = 4.2
num_cycles = 1
charge_current = 1.656
discharge_current = 1.656
rest_time = 30 * 60

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568 # conditions in the literature source. Guo et al

# Setup battery components
cell = BatteryCell(filepath_p=TEST_POS_ELEC_DIR, SOC_init_p=SOC_init_p, func_OCP_p=funcs.OCP_ref_p,
                        func_dOCPdT_p=funcs.dOCPdT_p, filepath_n = TEST_NEG_ELEC_DIR, SOC_init_n=SOC_init_n,
                        func_OCP_n=funcs.OCP_ref_n, func_dOCPdT_n=funcs.dOCPdT_n,
                        filepath_electrolyte = TEST_ELECTROLYTE_DIR, filepath_cell = TEST_BATTERY_CELL_DIR, T=T)
model = SPModel(isothermal=False, degradation=True)
SEI_model = ROM_SEI(bCell= cell, file_path= SEI_DIR, resistance_init=1e-12)

# set-up solver and solve
cycler = CC(num_cycles=num_cycles, charge_current=charge_current, discharge_current=discharge_current,
            rest_time=rest_time, V_max=V_max, V_min=V_min)
solver = EigenFuncExp(b_cell= cell, b_model= model, N=5, SEI_model=SEI_model)
sol = solver.solve(cycler=cycler, sol_name='test')

# Plot
sol.comprehensive_plot()