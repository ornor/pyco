import pyco.model as pycom

class Materiaal(pycom.BasisObject):
    """Betreft een materiaal met diverse eigenschappen.

    AANMAKEN MATERIAAL
        m1 = Materiaal()            invoeren van vorm objecten

    """

    def __init__(self):
        super().__init__()

        self._E = pycom.Waarde(0, 'N/m2')     # elasticiteitsmodulus
        self._G = pycom.Waarde(0, 'N/m2')     # glijdingsmodulus, alleen lezen
        self._v = pycom.Waarde(0)             # dwarscontractiecoefficient
        self._sm = pycom.Waarde(0, 'kg/m3')   # soortelijke massa
        self._sg = pycom.Waarde(0, 'N/m3')    # soortelijk gewicht

    def _check_waarde(self, waarde, zelfde_eenheid):
        if not isinstance(waarde, pycom.Waarde):
            raise TypeError('parameter is geen waarde object')
        if not waarde & zelfde_eenheid:
            raise ValueError('type eenheid van waarde is incorrect')

    @property
    def E(self):
        """Elasticiteitsmodulus."""
        return self._E
    @E.setter
    def E(self, waarde):
        self._check_waarde(waarde, self._E)
        self._E = waarde

    @property
    def G(self):
        """Glijdingsmodulus.
        https://nl.wikipedia.org/wiki/Schuifmodulus
        """
        return self.E[''] / (2 * (pycom.Waarde(1) + self.v)) # TODO
    @G.setter
    def G(self, waarde):
        raise Exception('Glijdingsmodulus is alleen lezen en wordt bepaald uit de waarde van elasticiteitsmodulus en de dwarscontractiecoefficient.')

    @property
    def v(self):
        """Dwarscontractiecoëfficiënt (Poisson factor)."""
        return self._v
    @v.setter
    def v(self, waarde):
        self._check_waarde(waarde, self._v)
        if float(waarde) == -1:
            raise ValueError('een dwarscontractiecoefficient van -1 leidt tot een glijdingsmodulus van oneindig groot; deze waarde is niet mogelijk')
        self._v = waarde

    @property
    def sm(self):
        """Soortelijke massa (dichtheid)."""
        return self._sm
    @sm.setter
    def sm(self, waarde):
        self._check_waarde(waarde, self._sm)
        self._sm = waarde

    @property
    def sg(self):
        """Soortelijk gewicht."""
        return self._sg
    @sg.setter
    def sg(self, waarde):
        self._check_waarde(waarde, self._sg)
        self._sg = waarde


if __name__ == '__main__':
    m1 = Materiaal()
    print(m1.E, bool(m1.E))
    m1.E = pycom.Waarde(2.1e5, 'MPa')
    m1.v = pycom.Waarde(0.2)
    m1.sm = pycom.Waarde(700e3, 'kg/m3')
    m1.sg = pycom.Waarde(75, 'kN/m3')
    print(m1.E, bool(m1.E))
    print(m1.G)
