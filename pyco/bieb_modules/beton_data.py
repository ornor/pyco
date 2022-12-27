import pyco as pc

class BetonMateriaalEigenschappen(pc.Data, pc.BiebItem):
    def __new__(cls):
        return pc.Data(
            sterkteklasse=None, f_ck='N/mm2', f_cd='N/mm2', f_ctd='N/mm2', f_ctm='N/mm2',
            E_cm='N/mm2', epsilon_c3=None, epsilon_cu3=None, alpha=None, beta=None,
            data = (
                ('C12/15', 12,  8.0, 0.73, 1.57, 27000, 0.00175, 0.00350, 0.75, 0.39),
                ('C16/20', 16, 10.7, 0.89, 1.90, 29000, 0.00175, 0.00350, 0.75, 0.39),
                ('C20/25', 20, 13.3, 1.03, 2.21, 30000, 0.00175, 0.00350, 0.75, 0.39),
            )
        )
