from typing import Union

from pyco.model import Vorm, Lijn

class Cirkel(Vorm):
    """Creeert een cirkelvormig Vorm object."""

    def __init__(self,
                 straal:Union[float, int]):

        lijn = Lijn([-1*straal, 0]).lijn_cirkelboog(
                    middelpunt=(0,0),
                    gradenhoek=360,
                    stappen=200,
                )
        super().__init__(lijn)
