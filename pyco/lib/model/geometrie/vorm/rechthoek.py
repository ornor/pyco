from typing import Union

from pyco.model import Vorm, Lijn

class Rechthoek(Vorm):
    """Creeert een rechthoekig Vorm object."""

    def __init__(self,
                 breedte:Union[float, int],
                 hoogte:Union[float, int]):

        lijn = Lijn([
                [-1/2 * breedte, -1/2 * hoogte],
                [-1/2 * breedte,  1/2 * hoogte],
                [ 1/2 * breedte,  1/2 * hoogte],
                [ 1/2 * breedte, -1/2 * hoogte],
            ])
        super().__init__(lijn)
