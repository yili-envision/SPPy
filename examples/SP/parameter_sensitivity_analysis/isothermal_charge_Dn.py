import SPPy


# Operating parameters
I = 1.656
T = 298.15
V_max = 4.05
SOC_min = 0.1
SOC_LIB = 0.9

# Modelling parameters
SOC_init_p, SOC_init_n = 0.989011, 0.01890232

# Setup battery components
lst_sol = []
for i in range(1, 8):
    cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
    cell.elec_n.D_ref = i * 0.5e-14
    dc = SPPy.Charge(charge_current=I, V_max=V_max, SOC_max=1, SOC_LIB=0)
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')
    sol = solver.solve(cycler_instance=dc, sol_name=f"$D_{{s,n}}={cell.elec_n.D_ref}$")
    lst_sol.append(sol)

# Plot
SPPy.Plots(lst_sol[0],
           lst_sol[1],
           lst_sol[2],
           lst_sol[3],
           lst_sol[4],
           lst_sol[5],
           lst_sol[6]).comprehensive_plot(save_fig='G:\My Drive\Writings\Electrochemical_models\SPM\sensitivity_Dn_charge.png')