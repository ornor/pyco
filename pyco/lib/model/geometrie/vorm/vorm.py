from typing import Union

import numpy as np
import matplotlib.pyplot as plt

from pyco.model import BasisObject, Waarde, Vector, Lijn, Knoop


class Vorm(BasisObject):
    """Betreft een meetkundig 2D vorm met bijbehorende eigenschappen.

    AANMAKEN VORM               invoeren van één Lijn object
        v1 = Vorm(Lijn(), translatie=, rotatie=, schaal=)


    """

    def __init__(self,
                 lijn:Lijn,
                 translatie:Vector=None,
                 rotatie:Union[Waarde, float, int]=None,
                 rotatiepunt:Knoop=None,
                 schaal:Union[Waarde, float, int]=None,
                 schaalpunt:Knoop=None):
        super().__init__()

        if not isinstance(lijn, Lijn):
            lijn = Lijn(*lijn)

        self._eenheid = lijn.eenheid
        self._array = lijn.array.copy()

        if self[0].tolist() != self[-1].tolist():
            # zorgen dat lijn gesloten is
            self._array = np.append(self._array,
                                    [self[0].tolist()],
                                    axis=0)

        # TODO checken dat geen enkele lijn een andere lijn kruist!!

        self.transformeren(translatie,
                           rotatie, rotatiepunt,
                           schaal, schaalpunt)

    @property
    def eenheid(self) -> str:
        """Geeft eenheid van Waarde. 'None' als geen eenheid."""
        return self._eenheid

    @eenheid.setter
    def eenheid(self, eenheid:str):
        """Zet knopen om naar nieuwe eenheid."""
        tmp_knopen = []
        oude_eenheid = self._eenheid

        for k_array in self.array:
            k = Knoop(k_array.tolist())
            k.eenheid = oude_eenheid
            k.eenheid = eenheid
            tmp_knopen.append(k.array.tolist())

        self._array = np.array(tmp_knopen, dtype='float64')
        self._eenheid = eenheid

    @property
    def array(self) -> np.array:
        """Retourneert Numpy array object met alle getallen (zonder eenheid)."""
        return self._array

    def transformeren(self,
                      translatie:Vector=None,
                      rotatie:Union[Waarde, float, int]=None,
                      rotatiepunt:Knoop=None,
                      schaal:Union[Waarde, float, int]=None,
                      schaalpunt:Knoop=None):
        """Verplaatst, roteert en/of verschaalt de vorm."""
        pass

    def plot(self):
        """Teken simpele plot van lijn (met 2 dimensies)."""
        plt.plot(self.array[:,0], self.array[:,1])
        plt.axis('equal')
        plt.show()

    @property
    def A(self) -> float:
        """Berekent oppervlakte en retourneert een float object."""
        opp = []

        for i in range(len(self)):
            opp.append(self[i][0]*self[i+1][1] - self[i+1][0]*self[i][1])

        opp_totaal = 1/2*sum(opp)
        return opp_totaal

    @property
    def A_(self) -> Waarde:
        """Berekent oppervlakte en retourneert een Waarde object."""
        w = Waarde(self.A)
        if self.eenheid is not None:
            opp_eenheid = '{}2'.format(self.eenheid)
            w[opp_eenheid]
        return w

    @property
    def z(self) -> list:
        """Berekent zwaartepunt in twee dimensies en retourneert een list met float."""
        z1 = []
        z2 = []

        for i in range(len(self)):
            z1.append((self[i][0] + self[i+1][0]) * (self[i][0]*self[i+1][1] - self[i+1][0]*self[i][1]))
            z2.append((self[i][1] + self[i+1][1]) * (self[i][0]*self[i+1][1] - self[i+1][0]*self[i][1]))

        z1_totaal = 1/(6*self.A)*sum(z1)
        z2_totaal = 1/(6*self.A)*sum(z2)

        return [z1_totaal, z2_totaal]

    @property
    def z_(self) -> Knoop:
        """Berekent zwaartepunt in twee dimensies en retourneert een Knoop object."""
        k = Knoop(self.z)
        k.eenheid = self.eenheid
        return k

    @property
    def O(self) -> float:
        """Berekent omtrek en retourneert een float."""
        return float(Lijn(self.array.tolist()))

    @property
    def O_(self) -> Waarde:
        """Berekent omtrek en retourneert een Waarde object."""
        return Waarde(self.O, self.eenheid)

    def __getitem__(self, index):
        """Retourneert subset Numpy array object met getallen (zonder eenheid)."""
        return self.array[index]

    def __len__(self):
        """Geeft aantal knopen."""
        # laatste knoop is zelfde als eerste knoop
        return len(self.array) - 1
