import SPPy


# Operating parameters
I = 0.1
T = 298.15
V_min = 2.5
SOC_min = 0
SOC_LIB = 1

# Modelling parameters
SOC_n_min = 0.01098666
SOC_n_max = 0.7953467
SOC_p_min = 0.43144714
SOC_p_max = 0.90469321

SOC_init_p, SOC_init_n = SOC_p_min, SOC_n_max  # from GA results


# Setup battery components
cell = SPPy.BatteryCell(parameter_set_name='Calce_NMC_18650', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
cell.elec_n.R =12.26e-6
cell.elec_p.R = 9.268e-6

# set-up cycler and solver
dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB)
solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly',
                         type='higher')

# simulate and save
sol = solver.solve(cycler_instance=dc, verbose='True', t_increment=1)
sol.save_instance('sol_discharge')

# Plot
# sol.comprehensive_plot()