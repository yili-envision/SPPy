from dataclasses import dataclass

from SPPy.battery_components import electrolyte, electrode


@dataclass
class BatteryCellBase:
    T_: float  # battery cell temperature, K
    rho: float  # battery density (mostly for thermal modelling), kg/m3
    Vol: float  # battery cell volume, m3
    C_p: float  # specific heat capacity, J / (K kg)
    h: float  # heat transfer coefficient, J / (S K)
    A: float  # surface area, m2
    cap: float  # capacity, Ah
    V_max: float  # maximum potential
    V_min: float  # minimum potential

    elec_p: electrode.PElectrode  # electrode class object
    elec_n: electrode.NElectrode  # electrode class object
    electrolyte: electrolyte.Electrolyte  # electrolyte class object

    def __post_init__(self):
        # self.T_ = self.T
        self.T_amb_ = self.T  # initial condition
        # initialize internal cell resistance
        self.R_cell = (self.elec_p.L / self.elec_p.kappa_eff + self.electrolyte.L / self.electrolyte.kappa_eff + \
                       self.elec_n.L / self.elec_n.kappa_eff) / self.elec_n.A
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


class BatteryCell(BatteryCellBase):
    """
    Class for the BatteryCell object and contains the relevant parameters.
    """

    def __init__(self, filepath_p, SOC_init_p, func_OCP_p, func_dOCPdT_p,
                 filepath_n, SOC_init_n, func_OCP_n, func_dOCPdT_n,
                 filepath_electrolyte, filepath_cell,
                 T):
        df = electrode.Electrode.parse_csv(file_path=filepath_cell)
        rho = df['Density [kg m^-3]']
        Vol = df['Volume [m^3]']
        C_p = df['Specific Heat [J K^-1 kg^-1]']
        h = df['Heat Transfer Coefficient [J s^-1 K^-1]']
        A = df['Surface Area [m^2]']
        cap = df['Capacity [A hr]']
        V_max = df['Maximum Potential Cut-off [V]']
        V_min = df['Minimum Potential Cut-off [V]']
        # initialize electrodes and electrolyte
        elec_p = electrode.PElectrode(file_path=filepath_p, SOC_init=SOC_init_p, T=T, func_OCP=func_OCP_p,
                                      func_dOCPdT=func_dOCPdT_p)
        elec_n = electrode.NElectrode(file_path=filepath_n, SOC_init=SOC_init_n, T=T, func_OCP=func_OCP_n,
                                      func_dOCPdT=func_dOCPdT_n)
        electrolyte_ = electrolyte.Electrolyte(file_path=filepath_electrolyte)
        super().__init__(T_=T, rho=rho, Vol=Vol, C_p=C_p, h=h, A=A, cap=cap, V_max=V_max, V_min=V_min, elec_p=elec_p,
                         elec_n=elec_n, electrolyte=electrolyte_)
