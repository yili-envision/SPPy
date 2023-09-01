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