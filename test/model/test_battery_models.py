import unittest

import SPPy
from SPPy.models import battery


class TestSPModel(unittest.TestCase):

    def test_m(self):
        T = 298.15
        # SOC_init_p = 0.4956
        SOC_init_p = 0.6
        # SOC_init_n = 0.7568
        SOC_init_n = 0.7
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

        testmodel = single_particle_model.SPModel()
        self.assertEqual(-0.2893183331034342, testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc, test_cell.elec_p.SOC, test_cell.electrolyte.conc))
        self.assertEqual(-2.7018597575301726, testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc, test_cell.elec_n.SOC, test_cell.electrolyte.conc))

    def test_V(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        R_cell = 0.00148861
        I = -1.656
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

        testmodel = single_particle_model.SPModel()
        OCP_p = test_cell.elec_p.OCP
        OCP_n = test_cell.elec_n.OCP
        m_p = testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc, test_cell.elec_p.SOC,
                    test_cell.electrolyte.conc)
        m_n = testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc, test_cell.elec_n.SOC, test_cell.electrolyte.conc)
        self.assertEqual(4.032392212009281, testmodel.calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T=T, I=I))
        # change SOC
        test_cell.elec_p.SOC = 0.6
        test_cell.elec_n.SOC = 0.6
        OCP_p = test_cell.elec_p.OCP
        OCP_n = test_cell.elec_n.OCP
        m_p = testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc,
                          test_cell.elec_p.SOC,
                          test_cell.electrolyte.conc)
        m_n = testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc,
                          test_cell.elec_n.SOC, test_cell.electrolyte.conc)
        self.assertEqual(3.8782812640647926, testmodel.calc_cell_terminal_voltage(OCP_p, OCP_n, m_p, m_n, R_cell, T=T, I=I))


class TestSPMe(unittest.TestCase):
    def test_flux_method(self):
        I = -1.65  # m2
        S_p = 1.1167  # m2
        S_n = 0.7824  # m2
        self.assertEqual(-I/(96487*S_n), battery.SPMe.volumetric_molar_fux(I=I, S=S_n, electrode_type='n'))
        self.assertEqual(I/(96487*S_p), battery.SPMe.volumetric_molar_fux(I=I, S=S_p, electrode_type='p'))

    def test_as(self):
        epsilon_n = 0.59
        epsilon_p = 0.49
        R_n = 1.25e-5
        R_p = 8.5e-6
        self.assertEqual(3 * epsilon_n / R_n, battery.SPMe.a_s(epsilon=epsilon_n, R=R_n))
        self.assertEqual(3 * epsilon_p / R_p, battery.SPMe.a_s(epsilon=epsilon_p, R=R_p))

