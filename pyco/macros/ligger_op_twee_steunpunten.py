import pyco as pc

Wd = pc.Waarde
Ls = pc.Lijst


class Ligger_op_twee_steunpunten(pc.Macro):
    """
    Berekent snedekrachten in een ligger op twee steunpunten.
    
    voorbeeld = Ligger_op_twee_steunpunten(
            titel='Dit is een voorbeeld',
            lengte=Wd(10).m,
            nx=200,  # de ligger wordt standaard op 200 plaatsen doorgerekend
        ).toevoegen_F(
            F=Wd(4).kN, x=Wd(2).m
        ).toevoegen_q(
            q=Wd(3).kN_m, x1=Wd(1).m, x2=Wd(6).m
        )()
    
    print document:
        voorbeeld.document()
        
    plot alleen pc.Figuur objecten:
        voorbeeld.invoer.geometrie.plot()
        voorbeeld.berekening.V_lijn.plot()
        voorbeeld.berekening.M_lijn.plot()
        
    voorbeeld: retourneer pc.Waarde object met maximaal moment:
        voorbeeld.berekening.M_max
    """
    
    def __init__(self, lengte=None, titel=None, nx=200):
        super().__init__()
        self.document = pc.Document('Ligger op twee steunpunten' if titel is None else titel)
        self.lengte = 1 if lengte is None else lengte
        self.F_data = []
        self.q_data = []
        self.nx = nx
        
    def toevoegen_F(self, F, x):
        self.F_data.append((F, x))
        return self
        
    def toevoegen_q(self, q, x1, x2):
        self.q_data.append((q, x1, x2))
        return self
    
    def __call__(self):
        doc = self.document

        @doc
        class invoer:
            L = Wd(self.lengte).m   >>\
            'lengte van ligger (afstand tussen de twee steunpunten)'

            F = Ls([F for F, _ in self.F_data]).kN   >>\
            'grootte van puntlast(en)'
            x_F = Ls([x for _, x in self.F_data]).m   >>\
            'afstand van linker steunpunt (A) tot aan puntlast(en)'

            q = Ls([q for q, _, _ in self.q_data]).kN_m   >>\
            'grootte van gelijkmatig verdeelde belasting'
            x1_q = Ls([x1 for _, x1, _ in self.q_data]).m   >>\
            'afstand van linker steunpunt (A) tot aan begin (linker kant) belasting'
            x2_q = Ls([x2 for _, _, x2 in self.q_data]).m   >>\
            'afstand van linker steunpunt (A) tot aan einde (rechter kant) belasting'

            # weergeven geometrie in figuur:

            _fL = float(L)  # lengte in meters
            _dx = _fL/30  # horizontale schaalfactor
            _dy = max(float(max(F) if len(F)>0 else 0),
                      float(max(q) if len(q)>0 else 0)) / 10  # verticale schaalfactor
            _coords_F = []
            for _F, _x_F in zip(F, x_F):
                _F = float(_F)
                _x_F = float(_x_F)
                _coords_F.append(( (_x_F, _F),
                                   (_x_F, 0),
                                   (_x_F-_dx, _dy),
                                   (_x_F, 0),
                                   (_x_F+_dx, _dy), ))
            _coords_q = []
            for _q, _x1_q, _x2_q in zip(q, x1_q, x2_q):
                _q = float(_q)
                _x1_q = float(_x1_q)
                _x2_q = float(_x2_q)
                _coords_q.append(( (_x1_q, _q),
                                   (_x1_q, 0),
                                   (_x1_q-_dx, _dy),
                                   (_x1_q, 0),
                                   (_x1_q+_dx, _dy), 
                                   (_x1_q, 0),
                                   (_x2_q, 0),
                                   (_x2_q-_dx, _dy),
                                   (_x2_q, 0),
                                   (_x2_q+_dx, _dy),
                                   (_x2_q, 0),
                                   (_x2_q, _q),
                                   (_x1_q, _q), ))

            geometrie = pc.Figuur(
                breedte=8,
                hoogte=4,
                raster=True,
            ).lijn(
                coordinaten=((0,0), (_fL,0)),
                kleur='red',
                breedte=4,
            ).lijn(
                coordinaten=((0,0), (-_dx,-_dy), (_dx, -_dy), (0,0)),
                kleur='red',
                breedte=1,
            ).lijn(
                coordinaten=((_fL,0), (_fL-_dx,-_dy), (_fL+_dx,-_dy), (_fL,0)),
                kleur='red',
                breedte=1,
            )
            for sub_coords in _coords_q:
                geometrie.lijn(
                    coordinaten=sub_coords,
                    kleur='olive',
                    breedte=2,
                    arcering='|',
                )
            for sub_coords in _coords_F:
                geometrie.lijn(
                    coordinaten=sub_coords,
                    kleur='blue',
                    breedte=2,
                )
                
        self.invoer = invoer

        @doc
        class berekening:
            n_x = self.nx  # aantal horizontale intervallen

            x = pc.van_totmet_n(Wd(0).m, invoer.L, n_x)   >>\
            'alle x-waarden waar snedekrachten berekend worden'

            dx = (x.i(1) - x.i(0)).mm   >>\
            'foutmarge van x-waarden'

            F_A = Wd(0).kN   >>\
            'container voor gesommeerde reactiekrachten in linker scharnier (A)'

            F_B = Wd(0).kN   >>\
            'container voor gesommeerde reactiekrachten in rechter scharnier (B)'

            V = Ls((x * 0).array).kN   >>\
            'container voor gesommeerde dwarskrachten'

            M = Ls((x * 0).array).kNm  >>\
            'container voor gesommeerde momenten'

            def VM_F(L, x, F, x_F):
                """Bepaalt dwarskracht en buigend moment in snede per puntlast."""

                F_A = (((L - x_F) / L) * F).kN   >>\
                'grootte reactiekracht linker steunpunt (A)'

                F_B = ((x_F / L) * F).kN   >>\
                'grootte reactiekracht rechter steunpunt (B)'

                V = F_A - pc.stap(x - x_F) * F   >>\
                'dwarskracht in snede x:<br/>$V(x) = - \\int q(x) \\; dx$'

                M = V.cumulatief() * (x.i(1) - x.i(0))   >>\
                'buigend moment in snede x:<br/>$M(x) = \\int V(x) \\; dx$'

                return F_A, F_B, V, M

            def VM_q(L, x, q, x1_q, x2_q):
                """Bepaalt dwarskracht en buigend moment in snede per gelijkmatig verdeelde last."""

                F_A = (((L - (x1_q + x2_q)/2) / L) * (q * (x2_q - x1_q))).kN   >>\
                'grootte reactiekracht linker steunpunt (A)'

                F_B = (((x1_q + x2_q)/2 / L) * (q * (x2_q - x1_q))).kN   >>\
                'grootte reactiekracht rechter steunpunt (B)'

                V = (F_A - pc.stap(x - x1_q) * (q * (x - x1_q))
                        + pc.stap(x - x2_q) * (q * (x - x2_q)))   >>\
                'dwarskracht in snede x:<br/>$V(x) = - \\int q(x) \\; dx$'

                M = V.cumulatief() * (x.i(1) - x.i(0))   >>\
                'buigend moment in snede x:<br/>$M(x) = \\int V(x) \\; dx$'

                return F_A, F_B, V, M

            for _F, _x_F in zip(invoer.F, invoer.x_F):
                _F_A, _F_B, _V, _M = VM_F(invoer.L, x, _F, _x_F)
                F_A += _F_A
                F_B += _F_B
                V += _V
                M += _M

            for _q, _x1_q, _x2_q in zip(invoer.q, invoer.x1_q, invoer.x2_q):
                _F_A, _F_B, _V, _M = VM_q(invoer.L, x, _q, _x1_q, _x2_q)
                F_A += _F_A
                F_B += _F_B
                V += _V
                M += _M

            V_lijn = pc.Figuur(
                breedte=8,
                hoogte=4,
                raster=True,
                titel='V-lijn',
            ).lijn(
                coordinaten=((0,0), *tuple(zip(x.array, V.array)), (float(invoer.L),0), (0,0)),
                breedte=2,
                arcering='/',
            )

            V_min = min(V)
            V_min_x = x.i(V.array.tolist().index(V_min))

            V_max = max(V)
            V_max_x = x.i(V.array.tolist().index(V_max))

            M_lijn = pc.Figuur(
                breedte=8,
                hoogte=4,
                raster=True,
                titel='M-lijn',
                spiegel_y_as=True,
            ).lijn(
                coordinaten=((0,0), *tuple(zip(x.array, M.array)), (float(invoer.L),0), (0,0)),
                breedte=2,
                arcering='/',
            )

            M_min = min(M)
            M_min_x = x.i(M.array.tolist().index(M_min))

            M_max = max(M)
            M_max_x = x.i(M.array.tolist().index(M_max))

        self.berekening = berekening
        
        return self