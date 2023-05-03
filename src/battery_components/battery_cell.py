from src.battery_components import electrolyte,electrode


class BatteryCell:
    def __init__(self, filepath_p, SOC_init_p, func_OCP_p, func_dOCPdT_p,
                 filepath_n, SOC_init_n, func_OCP_n, func_dOCPdT_n,
                 filepath_electrolyte, filepath_cell,
                 T):
        # initialize cell parameters
        self.T_ = T
        self.T_amb_ = T # initial condition
        df = electrode.Electrode.parse_csv(file_path=filepath_cell)
        # print(df)
        self.rho = df['Density [kg m^-3]']
        self.Vol = df['Volume [m^3]']
        self.C_p = df['Specific Heat [J K^-1 kg^-1]']
        self.h = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        self.A = df['Surface Area [m^2]']
        self.cap = df['Capacity [A hr]']
        self.V_max = df['Maximum Potential Cut-off [V]']
        self.V_min = df['Minimum Potential Cut-off [V]']
        # initialize electrodes and electrolyte
        self.elec_p = electrode.PElectrode(file_path=filepath_p, SOC_init=SOC_init_p, T=T, func_OCP=func_OCP_p,
                                          func_dOCPdT=func_dOCPdT_p)
        self.elec_n = electrode.NElectrode(file_path=filepath_n, SOC_init=SOC_init_n, T=T, func_OCP=func_OCP_n,
                                           func_dOCPdT=func_dOCPdT_n)
        self.electrolyte = electrolyte.Electrolyte(file_path=filepath_electrolyte)
        # initialize internal cell resistance
        self.R_cell = (self.elec_p.L/self.elec_p.kappa_eff + self.electrolyte.L/self.electrolyte.kappa_eff + self.elec_n.L/self.elec_n.kappa_eff) / self.elec_n.A
        self.R_cell_init = self.R_cell

    @property
    def T(self):
        return self.T_

    @T.setter
    def T(self, new_T):
        self.T_ = new_T
        self.elec_p.T = new_T
        self.elec_n.T = new_T

    @property
    def T_amb(self):
        return self.T_amb_
