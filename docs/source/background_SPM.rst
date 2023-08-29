===========================================================================
Background - Single Particle Model for Continuum Scale Lithium-Ion Models
===========================================================================

Fuller, Doyle, and Neumann reported an electrochemical model for LIBs, which is still widely used today.
The model uses the mass and charge conservation partial differential equations (PDEs) in both the solid
(positive and negative electrodes) and solution phase (electrolyte in the positive electrode,  separator,
and negative electrode regions). These PDEs are coupled by the Butler-Volmer equation (BV), which models the flux of
the lithium-ion across the electrode-electrolyte region. The PDEs are usually solved in 1D across the thickness of
the battery cell, while the electrode particles are modeled in the spherical coordinates. For this reason, the
model is also referred to as the Pseudo-2D (P2D) model [1]. The resulting equations
can be numerically (e.g., finite differences, finite volume [2], and finite element approaches.)
solved at discrete spatial and temporal points. However due to the relative difficultly of implementation and the
required computation resource required, a simpler single particle model (SPM) has also been used for battery cell
simulations. SPM ignores the electrolyte dynamics during the battery operations. The result is a single PDE and an
algebraic equation [3]. Electrochemical models, including SPM and P2D models, model the cell terminal
voltage taking into account. Thermal and battery cell degradation models can be incorporated with these models [4, 5].

References
=============

#. Thomas F. Fuller, Marc Doyle, and John Newman. “Simulation and Optimization of the Dual
   Lithium Ion Insertion Cell”. In: Journal of The Electrochemical Society 141.1 (Jan. 1994),
   pp. 1–10. doi: 10.1149/1.2054684.
#. Marcello Torchio et al. “LIONSIMBA: A Matlab Framework Based on a Finite Volume Model
   Suitable for Li-Ion Battery Design, Simulation, and Control”. In: Journal of The Electrochemical
   Society 163.7 (2016), A1192–A1205. doi: 10.1149/2.0291607jes.
#. James L. Lee, Andrew Chemistruck, and Gregory L. Plett. “One-dimensional physics-based
   reduced-order model of lithium-ion dynamics”. In: Journal of Power Sources 220 (Dec. 2012),
   pp. 430–448. doi: 10.1016/j.jpowsour.2012.07.075.
#. Meng Guo, Godfrey Sikha, and Ralph E. White. “Single-Particle Model for a Lithium-Ion Cell:
   Thermal Behavior”. In: Journal of The Electrochemical Society 158 (2 Dec. 2011), A122. issn:
   00134651. doi: 10.1149/1.3521314/XML.
#. Simon E. J. O’Kane et al. “Lithium-ion battery degradation: how to model it”. In: Physical
   Chemistry Chemical Physics 24.13 (2022), pp. 7909–7922. doi: 10.1039/d2cp00417h.
