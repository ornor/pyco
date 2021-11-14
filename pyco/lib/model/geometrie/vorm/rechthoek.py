from typing import Union

from pyco.model import Vorm, Lijn, Waarde

class Rechthoek(Vorm):
    """Creeert een rechthoekig Vorm object."""

    def __init__(self,
                 breedte:Union[Waarde, float, int],
                 hoogte:Union[Waarde, float, int]):

        eenheid = None
        if isinstance(breedte, Waarde):
            eenheid = breedte.eenheid
        b = float(breedte)

        if isinstance(hoogte, Waarde):
            hoogte.eenheid = eenheid
        h = float(hoogte)

        lijn = Lijn([
                [-1/2 * b, -1/2 * h],
                [-1/2 * b,  1/2 * h],
                [ 1/2 * b,  1/2 * h],
                [ 1/2 * b, -1/2 * h],
            ])
        lijn.eenheid = eenheid

        super().__init__(lijn)
