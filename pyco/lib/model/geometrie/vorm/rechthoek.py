from typing import Union

import pyco.model as pycom

class Rechthoek(pycom.Vorm):
    """Creeert een rechthoekig Vorm object."""

    def __init__(self,
                 breedte:Union[pycom.Waarde, float, int],
                 hoogte:Union[pycom.Waarde, float, int]):

        eenheid = None
        if isinstance(breedte, pycom.Waarde):
            eenheid = breedte.eenheid
        b = float(breedte)

        if isinstance(hoogte, pycom.Waarde):
            hoogte.eenheid = eenheid
        h = float(hoogte)

        lijn = pycom.Lijn([
                [-1/2 * b, -1/2 * h],
                [-1/2 * b,  1/2 * h],
                [ 1/2 * b,  1/2 * h],
                [ 1/2 * b, -1/2 * h],
            ])
        lijn.eenheid = eenheid

        super().__init__(lijn)
