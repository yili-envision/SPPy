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

        testmodel = battery.SPM()
        self.assertEqual(-0.2893183331034342, testmodel.m(-1.656, test_cell.elec_p.k, test_cell.elec_p.S, test_cell.elec_p.max_conc, test_cell.elec_p.SOC, test_cell.electrolyte.conc))
        self.assertEqual(-2.7018597575301726, testmodel.m(-1.656, test_cell.elec_n.k, test_cell.elec_n.S, test_cell.elec_n.max_conc, test_cell.elec_n.SOC, test_cell.electrolyte.conc))

    def test_V(self):
        T = 298.15
        SOC_init_p = 0.4956
        SOC_init_n = 0.7568
        R_cell = 0.00148861
        I = -1.656
        test_cell = SPPy.BatteryCell(parameter_set_name='test', SOC_init_p=SOC_init_p, SOC_init_n=SOC_init_n, T=T)

        testmodel = battery.SPM()
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


class TestESP(unittest.TestCase):
    def test_molar_flux(self):
        I = -1.656
        S = 0.7824
        self.assertEqual(2.1936265167099342e-05, battery.SPMe.molar_flux_electrode(I=I, S=S, electrode_type='n'))
        self.assertEqual(-2.1936265167099342e-05, battery.SPMe.molar_flux_electrode(I=I, S=S, electrode_type='p'))

    def test_i_0(self):
        k = 1.764e-11
        c_s_max = 31833
        c_e = 1000
        soc_surf = 0.5
        self.assertEqual(8.878634015491551e-06, battery.SPMe.i_0(k=k, c_s_max=c_s_max, c_e=c_e, soc_surf=soc_surf))

    def test_eta(self):
        j = 2.1936265167099342e-05
        i_0_ = 8.878634015491551e-06
        temp = 298.15
        self.assertEqual(0.05335777844201581, battery.SPMe.eta(temp=temp, j=j, i_0_=i_0_))

    def test_calc_terminal_voltage(self):
        ocp_p = 4.2
        ocp_n = 0.15
        eta_p = 0.05
        eta_n = 0.05
        l_p = 7.35E-05
        l_sep = 2.00E-05
        l_n = 7.00E-05
        battery_cross_area = 0.0596
        kappa_eff_avg = 0.2
        t_c = 0.38
        R_p = 0.0
        R_n = 0.0
        S_p = 1.1167
        S_n = 0.7824
        c_e_n = 1100
        c_e_p = 900
        i_app = -1.656

        print(battery.SPMe.calc_terminal_voltage(ocp_p=ocp_p, ocp_n=ocp_n, eta_p=eta_p, eta_n=eta_n, l_p=l_p,
                                                 l_sep=l_sep, l_n=l_n, battery_cross_area=battery_cross_area,
                                                 kappa_eff_avg=kappa_eff_avg, t_c=t_c, R_p=R_p, R_n=R_n,
                                                 S_p=S_p, S_n=S_n, c_e_n=c_e_n, c_e_p=c_e_p, i_app=i_app, k_f_avg=5,
                                                 temp=298.15))

