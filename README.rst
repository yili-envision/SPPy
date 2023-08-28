**************************************************************************************
Lithium-Ion Battery Cell Terminal Models coupled with Thermal and Degradation Models
**************************************************************************************

Copyright© 2023 by Moin Ahmed. All rights reserved.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

==================================================================
Description
==================================================================

This repository contains the code for running equivalent circuit model (ECM) and single particle model (SPM) with thermal and degradation models on
Lithium-ion Batteries (LIB). Moreover, the repository contains the tools for visualization and
parameter estimations (using genetic algorithm).


All the code is written in Python programming language, and it is written in a modular fashion. The code is
still an ongoing work and the documentation is not yet complete.

==================================================================
Features
==================================================================

* Single Particle Model (SPM) and Equivalent circuit model (ECM) with thermal (lumped thermal) and degradation (reduced-order SEI) models
    .. image:: ../../Assests/SPPy.png
* Parameter estimation using genetic algorithm
* Visualization tools
* Sigma Point Kalman Filter (for analyzing application' battery management system (BMS))

==================================================================
Dependencies
==================================================================
#. Python 3.10 and above
#. numpy
#. pandas
#. matplotlib
#. scipy
#. tqdm

==================================================================
Installation
==================================================================

Either of the two recommended installation procedures can be used and the steps for these
installation procedures are listed below.

Git Clone
************************

#. Install external python package dependencies required for this repository. The required dependencies are:

    * numpy

    * pandas

    * matplotlib

    * scipy

    * tqdm

#. Clone the repository, for example using git clone `repository link <git@github.com:m0in92/EV_sim.git>`_ using Git Bash.

Python setup
************************
#. Download or clone this repository
#. Ensure you are on the repository directory (where the setup.py resides) and run python setup.py sdist on the command line.
#. Step 2 will create a dist directory in the repository. Extract the contents tar.gz file in this directory. Move to
   the directory where the extracted files reside and run pip install EV_sim on the command line. This will install EV_sim
   on your system (along with the external dependencies) and EV_sim can be imported as any other Python package.

==================================================================
Sample Usage
==================================================================
The simulation consists of creating a (1) battery cell, (2) cycler, and (3) solver object. For the battery cell object,
the parameters can be read from the parameter sets.

The following gives an example of running a single particle model under isothermal conditions using the parameter_set
named "test".::

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
    sol.comprehensive_plot()
