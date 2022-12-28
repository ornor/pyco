import pyco as pc

class BetonEigenschappen(pc.Data, pc.BiebItem):
    def __new__(cls):
        return pc.Data(
            sterkteklasse=None, f_ck='MPa', f_ck_cube='MPa', f_cm='MPa', 
            f_ctm='MPa', f_ctk_005='MPa', f_ctk_095='MPa',
            E_cm='GPa', epsilon_c3='prom', epsilon_cu3='prom',
            data = (
                ('C12/15', 12, 15, 20, 1.6, 1.1, 2.0, 27, 1.75, 3.5),
                ('C16/20', 16, 20, 24, 1.9, 1.3, 2.5, 29, 1.75, 3.5),
                ('C20/25', 20, 25, 28, 2.2, 1.5, 2.9, 30, 1.75, 3.5),
                ('C25/30', 25, 30, 33, 2.6, 1.8, 3.3, 31, 1.75, 3.5),
                ('C30/37', 30, 37, 38, 2.9, 2.0, 3.8, 33, 1.75, 3.5),
                ('C35/45', 35, 45, 43, 3.2, 2.2, 4.2, 34, 1.75, 3.5),
                ('C40/50', 40, 50, 48, 3.5, 2.5, 4.6, 35, 1.75, 3.5),
                ('C45/55', 45, 55, 53, 3.8, 2.7, 4.9, 36, 1.75, 3.5),
                ('C50/60', 50, 60, 58, 4.1, 2.9, 5.3, 37, 1.75, 3.5),
                ('C55/67', 55, 67, 63, 4.2, 3.0, 5.5, 38, 1.8, 3.1),
                ('C60/75', 60, 75, 68, 4.4, 3.1, 5.7, 39, 1.9, 2.9),
                ('C70/85', 70, 85, 78, 4.6, 3.2, 6.0, 41, 2.0, 2.7),
                ('C80/95', 80, 95, 88, 4.8, 3.4, 6.3, 42, 2.2, 2.6),
                ('C90/105', 90, 105, 98, 5.0, 3.5, 6.6, 44, 2.2, 2.6),
            ),
            bronnen = ('NEN-EN 1992-1-1+C2:2011+NB:2007 tabel 3.1')
        )

class BetonMateriaalFactoren(pc.Data, pc.BiebItem):
    def __new__(cls):
        return pc.Data(
            materiaal=None, blijvend_tijdelijk=None,
            buitengewoon=None, vermoeiing=None,
            data = (
                ('beton', 1.5, 1.2, 1.35),
                ('betonstaal', 1.15, 1.0, 1.15),
                ('voorspanstaal', 1.1, 1.0, 1.1),
            ),
            bronnen = ('NEN-EN 1992-1-1+C2:2011+NB:2007 tabel 2.1N')
        )