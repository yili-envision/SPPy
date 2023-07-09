import unittest

import SPPy
from SPPy.models import single_particle_model


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
