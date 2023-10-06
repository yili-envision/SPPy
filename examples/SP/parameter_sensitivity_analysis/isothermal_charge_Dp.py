import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_min = 3
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al

# Setup battery components
lst_sol = []
for i in range(1, 8):
    cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
    cell.elec_p.D_ref = i * 0.5e-14
    dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')
    sol = solver.solve(cycler_instance=dc, sol_name=f"$D_{{s,p}}={cell.elec_p.D_ref}$")
    lst_sol.append(sol)

# Plot
SPPy.Plots(lst_sol[0],
           lst_sol[1],
           lst_sol[2],
           lst_sol[3],
           lst_sol[4],
           lst_sol[5],
           lst_sol[6]).comprehensive_plot(save_fig='G:\My Drive\Writings\Electrochemical_models\SPM\sensitivity_Dp_discharge.png')