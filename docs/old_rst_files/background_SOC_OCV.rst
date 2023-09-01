=========================================================================
Background - Lithium-Ion Battery Cell Open Circuit Voltage
=========================================================================

An electrode's state-of-charge(SOC) represents the ratio of the current surface lithium concentration and its maximum
lithium concentration capacity. During the battery operation, as the lithium inventory in the electrode keeps
changing, the electrode's lithium stoichiometry and SOC keeps changing. Furthermore, the electrode’s open circuit
potential (OCP), which denotes its thermodynamic equilibrium potential, is a function of its
SOC (Figure 1). Subsequently, the equilibrium potential of the LIB, open-circuit voltage (OCV),
is a difference between the positive and negative electrode’s OCP, i.e.,

.. math::
    OCV = OCP|_p - OCP|_n

.. figure:: Assests/background/OCP_SOC.png

    Representative $OCP$ vs. SOC for negative (left) and positive (right) electrode of a LIB with Lithium-Cobalt-Oxide
    positive electrode (the function representing relationship between the electrode's SOC and OCP is obtained
    from ref[1]). The arrow points to the direction of change of respective electrode's SOC during battery cell discharge.

References
===============
1. Meng Guo, Godfrey Sikha, and Ralph E. White. “Single-Particle Model for a Lithium-Ion Cell:
Thermal Behavior”. In: Journal of The Electrochemical Society 158 (2 Dec. 2011), A122. issn:
00134651. doi: 10.1149/1.3521314/XML.

.. toctree::
    :maxdepth: -1
    :caption: Contents:
