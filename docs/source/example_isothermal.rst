==================================================================
Example - Single Particle Model - Isothermal - Discharge Cycle
==================================================================
The simulation consists of creating a (1) battery cell, (2) cycler, and (3) solver object. For the battery cell object,
the parameters can be read from the parameter sets.

The following gives an example of running a single particle model under isothermal conditions using the parameter_set
named "Gao-Randall"::

    import SPPy
    </code></br></br></br>

    # Define operating parameters </br>
    I = 1.656 </br>
    T = 298.15 </br>
    V_min = 3 </br>
    SOC_min = 0.1 </br>
    SOC_LIB = 0.9 </br>
    </code></br>

    # Define modelling parameters </br>
    SOC_init_p, SOC_init_n = 0.4956, 0.7568  # conditions in the literature source. Guo et al
    </code></br></br>

    # Setup battery components </br>
    cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)
    </code></br>

    # set-up cycler and solver </br>
    dc = SPPy.Discharge(discharge_current=I, V_min=V_min, SOC_LIB_min=SOC_min, SOC_LIB=SOC_LIB) </br>
    solver = SPPy.SPPySolver(b_cell=cell, N=5, isothermal=True, degradation=False, electrode_SOC_solver='poly')
    </code></br>

The simulation will start once the ``solve`` method of the SPPySolver instance is called.
This method requires the cycler instance::

    # simulate
    sol = solver.solve(cycler_instance=dc)

The ``sol`` object stores various simulation results, including time, cell terminal voltage, electrode's lithium surface concentrations, etc.
Furthermore, it has plotting methods, for eg.,::

    # Plot </br>
    sol.comprehensive_isothermal_plot()

The following ``comprehensive_isothermal_plot()`` method outputs the following plot with the information on the cell
terminal potential during its discharge, as well the electrode's surface SOC.

.. image:: example_isothermal.png


.. toctree::
   :maxdepth: -1
   :caption: Contents:



