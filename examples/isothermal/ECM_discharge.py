import pickle

import scipy

import SPPy


with open("saved_results/SOC", "rb") as f_SOC:
    SOC = pickle.load(f_SOC)

with open("saved_results/OCV", "rb") as f_OCV:
    OCV = pickle.load(f_OCV)

with open("saved_results/SOC_dOCVdT", "rb") as f_SOC:
    SOC_dOCVdT = pickle.load(f_SOC)

with open("saved_results/dOCVdT", "rb") as f_OCV:
    dOCVdT = pickle.load(f_OCV)


def func_eta(SOC, temp):
    return 1


func_OCV = scipy.interpolate.interp1d(SOC, OCV, fill_value='extrapolate')
func_dOCVdT = scipy.interpolate.interp1d(SOC_dOCVdT, dOCVdT, fill_value='extrapolate')


# Simulation Parameters
I = 1.65
V_min = 2.5
SOC_min = 0
SOC_LIB = 1

# setup the battery cell
cell = SPPy.ECMBatteryCell(R0_ref=0.005, R1_ref=0.001, C1=0.03, temp_ref=298.15, Ea_R0=4000, Ea_R1=4000,
                           rho=1626, vol=3.38e-5, c_p=750, h=1, area=0.085, cap=1.65, v_max=4.2, v_min=2.5,
                           soc_init=0.98, temp_init=298.15, func_eta=func_eta, func_ocv=func_OCV, func_docvdtemp=func_dOCVdT)
# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.DTSolver(battery_cell_instance=cell, isothermal=True)
# solve
sol = solver.solve(cycling_step=dc)

# Plots
sol.comprehensive_plot()
