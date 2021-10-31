from typing import Union

import numpy as np
import matplotlib.pyplot as plt

from pyco.model import BasisObject, Waarde, Vector, Lijn, Knoop

class VormFuncties:
    """Statische hulpfuncties voor uitrekenen eigenschappen vorm."""

    @classmethod
    def punt_aan_linker_zijde(cls, la, lb, p):
        """Checkt of punt p aan linker kant van lijn la-lb ligt."""
        return (((lb[0] - la[0]) * (p[1] - la[1])
                 - (lb[1] - la[1]) * (p[0] - la[0])) > 0)

    @classmethod
    def punt_aan_rechter_zijde(cls, la, lb, p):
        """Checkt of punt p aan rechter kant van lijn la-lb ligt."""
        return (((lb[0] - la[0]) * (p[1] - la[1])
                 - (lb[1] - la[1]) * (p[0] - la[0])) < 0)

    @classmethod
    def punt_op_lijn(cls, la, lb, p):
        """Checkt of punt p op lijn la-lb ligt, tussen la en lb."""
        op_lijn = (((lb[0] - la[0]) * (p[1] - la[1])
                    - (lb[1] - la[1]) * (p[0] - la[0])) == 0)
        if not op_lijn:
            return False
        if la[0] == lb[0]:     # verticale lijn
            return ((p[1] <= lb[1] and p[1] >= la[1]) or
                    (p[1] >= lb[1] and p[1] <= la[1]))
        else:
            return ((p[0] <= lb[0] and p[0] >= la[0]) or
                    (p[0] >= lb[0] and p[0] <= la[0]))

    @classmethod
    def lijn_raakt_lijn(cls, l1a, l1b, l2a, l2b):
        """Checkt of lijn l1a-l1b de lijn l2a-l2b kruist of raakt, op de lijnstukken TUSSEN de punten en INCLUSIEF de punten zelf."""
        if (cls.punt_op_lijn(l1a, l1b, l2a) or
                cls.punt_op_lijn(l1a, l1b, l2b) or
                cls.punt_op_lijn(l2a, l2b, l1a) or
                cls.punt_op_lijn(l2a, l2b, l1b)):
            # uiteinde lijn ligt op andere lijn
            return True

        l1xmin = min(l1a[0], l1b[0])
        l1xmax = max(l1a[0], l1b[0])
        l2xmin = min(l2a[0], l2b[0])
        l2xmax = max(l2a[0], l2b[0])
        l1ymin = min(l1a[1], l1b[1])
        l1ymax = max(l1a[1], l1b[1])
        l2ymin = min(l2a[1], l2b[1])
        l2ymax = max(l2a[1], l2b[1])
        if (l1xmin > l2xmax or l2xmin > l1xmax or
                l1ymin > l2ymax or l2ymin > l1ymax):
            # lijn ligt helemaal links/rechts/onder/boven andere lijn
            return False

        # l1 = a * x + b
        # l2 = c * x + d
        if l1b[0] - l1a[0] == 0:        # l1 is een verticale lijn
            x = l1a[0]
            if l2b[0] - l2a[0] == 0: 	# l2 is ook verticaal
                return False
            else:
                c = 1.0 * (l2b[1] - l2a[1]) / (l2b[0] - l2a[0])
                d = l2a[1] - l2a[0] * c
                y = c * x + d
                if ((y >= l1a[1] and y <= l1b[1]) or
                         (y >= l1b[1] and y <= l1a[1])):
                    return True
                else:
                    return False
        elif l2b[0] - l2a[0] == 0:          # l2 is een verticale lijn
            x = l2a[0]
            if l1b[0] - l1a[0] == 0:	    # l1 is ook verticaal
                return False
            else:
                a = 1.0 * (l1b[1] - l1a[1]) / (l1b[0] - l1a[0])
                b = l1a[1] - l1a[0] * a
                y = a * x + b
                if ((y >= l2a[1] and y <= l2b[1]) or
                         (y >= l2b[1] and y <= l2a[1])):
                    return True
                else:
                    return False
        else:                           # beide lijnen zijn diagonaal
            a = 1.0 * (l1b[1] - l1a[1]) / (l1b[0] - l1a[0])
            b = l1a[1] - l1a[0] * a
            c = 1.0 * (l2b[1] - l2a[1]) / (l2b[0] - l2a[0])
            d = l2a[1] - l2a[0] * c
            # l1 gelijk aan l2
            if a - c == 0:              # parallel
                return False
            x = 1.0 * (d - b) / (a - c)
        if x >= l1xmin and x >= l2xmin and x <= l1xmax and x <= l2xmax:
            return True
        else:
            return False


class Vorm(BasisObject):
    """Betreft een meetkundig 2D vorm met bijbehorende eigenschappen.

    AANMAKEN VORM               invoeren van één Lijn object
        v1 = Vorm(Lijn(), translatie=, rotatie=, schaal=)


    """

    fn = VormFuncties()

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

    def __getitem__(self, index):
        """Retourneert subset Numpy array object met getallen (zonder eenheid)."""
        return self.array[index]

    def __len__(self):
        """Geeft aantal knopen."""
        # laatste knoop is zelfde als eerste knoop
        return len(self.array) - 1

    def __iter__(self):
        """Itereert over knopen en geeft Knoop objecten terug."""
        for k_array in self.array[:-1]:
            k = Knoop(k_array.tolist())
            k.eenheid = self.eenheid
            yield k

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
