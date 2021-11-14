from typing import Union
import math

from pyco.model import Vorm, Lijn, Waarde

class Cirkel(Vorm):
    """Creeert een cirkelvormig Vorm object."""

    def __init__(self,
                 straal:Union[float, int]):

        eenheid = None
        if isinstance(straal, Waarde):
            eenheid = straal.eenheid
        r = float(straal)

        lijn = Lijn([-1*r, 0]).lijn_cirkelboog(
                    middelpunt=(0,0),
                    gradenhoek=360,
                    stappen=200,
                )
        lijn.eenheid = eenheid

        super().__init__(lijn)

        # corrigeer benadering cirkel met polygoon door exacte waarde
        self.O = 2 * math.pi * r
        self.A = math.pi * r**2
        self.xmin = -r
        self.xmax = r
        self.ymin = -r
        self.ymax = r
        self.Ixx = 1/4 * math.pi * r**4
        self.Iyy = self.Ixx
        self.Ixy = 0.0
        self.I1 = self.Ixx
        self.I2 = self.Ixx
        self.alpha = 0.0
        self.Wxmin = self.Ixx / r
        self.Wxmax = self.Wxmin
        self.Wymin = self.Wxmin
        self.Wymax = self.Wxmin
        self.kxmin = -r / 4
        self.kxmax = r / 4
        self.kymin = self.kxmin
        self.kymax = self.kxmax

        self._bereken_waardes()
