import numpy as np
import matplotlib.pyplot as plt

import pyco.model as pycom


class Lijn(pycom.BasisObject):
    """Bevat een collectie met knopen, waartussen zich rechte lijnen bevinden.

    AANMAKEN LIJN               invoeren van één of meedere Knoop objecten
        Lijn(Knoop(Waarde(1).cm, Waarde(2).cm)))    begin Knoop object
        Lijn([1,2]) of Lijn((1,2))                  alleen begincoordinaat
        Lijn((1,2), (3,4), (5,6))                   alle knoopcoordinaten

    AANPASSEN EENHEID
        l = Lijn((1,2), (3,4))
        l.eenheid               opvragen huidige eenheid; in dit geval None
        l.eenheid = 'm'         alle waarden in alle knoopobjecten naar 'm'

    OMZETTEN LIJN NAAR TEKST    resulteert in nieuw string object
        tekst = str(l)          of automatisch met bijvoorbeeld print(l)
        tekst = format(l,'.2f') format configuratie meegeven voor getal

    VERLENGEN LIJN              vanuit laatste knoop (of enige beginknoop)
        l.lijn_recht(naar=(3,4))
            rechte lijn naar een nieuwe knoop

        l.lijn_bezier(richting=(3,4), naar=(5,6), stappen=100)
            (kwadratische) Bezier kromme (met één richtingspunt) naar nieuwe
            knoop waarbij de kromme lijn omgezet wordt in aantal (stappen)
            rechte lijnen; standaard 100 stappen

        l.lijn_cirkelboog(middelpunt=(3,4), gradenhoek=-90, stappen=100)
            cirkelboog met opgegeven cirkel middelpunt over aantal opgegeven
            graden (waarbij 360 is gehele cirkel tekenen; positief is tegen
            klok in; negatief getal is met de klok mee) waarbij kromme lijn
            omgezet wordt in aantal rechte lijnen; standaard 100 stappen

    MOGELIJKE BEWERKINGEN
        waarde = abs(l)         berekent lengte lijnstukken -> Waarde object
        getal = float(l)        berekent lengte lijnstukken -> float object
        for w in v1:            itereert en geeft Knoop object terug
        getal = len(v1)         geeft aantal knopen terug

    NUMPY BEWERKINGEN               gebruikt array object
        2D numpy_array = l1.array   retourneert volledige Numpy array object
                                      (bevat allen getallen, zonder eenheid)
        1D_numpy_array = l1[2]      retourneert knoopcoordinaten op index
        2D_numpy_array = l1[1:3]    retourneert knoopcoordinaten vanuit slice

    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        l1 == l2                is gelijk aan
        l1 != l2                is niet gelijk aan
        l1 &  l2                eenheden zijn zelfde type

    EXTRA OPTIES
        l.plot2d()              plot simpele weergave van lijn

        Lijn((4, -5), (-10, 10)).lijn_cirkelboog(middelpunt=(0,0),
            gradenhoek=+220, stappen=50).lijn_recht(naar=(4, 10)).lijn_bezier(
            richting=(-10,-4), naar=(4, -5)).plot2d()
    """

    def __init__(self, *knopen):
        super().__init__()

        tmp_knopen = []
        self._eenheid = None

        if (len(knopen) == 1
                and (
                    isinstance(knopen[0], list) or
                    isinstance(knopen[0], tuple))
                and len(knopen[0]) > 0
                and (
                    isinstance(knopen[0][0], pycom.Knoop) or
                    isinstance(knopen[0][0], list) or
                    isinstance(knopen[0][0], tuple))):
            knopen = knopen[0]

        if len(knopen) < 1:
            raise ValueError('voer minimaal één knoop in')

        for i, knoop in enumerate(knopen):
            if not (isinstance(knoop, pycom.Knoop)
                    or isinstance(knoop, list) or isinstance(knoop, tuple)):
                raise TypeError('opgegeven argument is geen Knoop object of lijst met getallen/Waardes')
            if not isinstance(knoop, pycom.Knoop):
                knoop = pycom.Knoop(knoop)
            if i > 0:
                if ((self._eenheid is None and knoop.eenheid is not None)
                        or (self._eenheid is not None and knoop.eenheid is None)):
                    raise ValueError('knopen moeten zelfde type eenheid hebben')
                knoop.eenheid = self._eenheid
            if i == 0 or (i > 0 and tmp_knopen[-1] != knoop.array.tolist()):
                tmp_knopen.append(knoop.array.tolist())
            if i == 0:
                self._eenheid = knoop.eenheid

        self._array = np.array(tmp_knopen, dtype='float64')

    @property
    def eenheid(self):
        """Geeft eenheid van Waarde. 'None' als geen eenheid."""
        return self._eenheid

    @eenheid.setter
    def eenheid(self, eenheid:str):
        """Zet knopen om naar nieuwe eenheid."""
        tmp_knopen = []
        oude_eenheid = self._eenheid

        for k_array in self.array:
            k = pycom.Knoop(k_array.tolist())
            k.eenheid = oude_eenheid
            k.eenheid = eenheid
            tmp_knopen.append(k.array.tolist())

        self._array = np.array(tmp_knopen, dtype='float64')
        self._eenheid = eenheid

    @property
    def array(self):
        """Retourneert Numpy array object met alle getallen (zonder eenheid)."""
        return self._array

    def lijn_recht(self, naar):
        """Verlengt lijn object met een extra rechte lijn naar opgegeven knoop."""
        if not (isinstance(naar, pycom.Knoop)
                or isinstance(naar, list) or isinstance(naar, tuple)):
            raise TypeError('opgegeven argument is geen Knoop object of lijst met getallen/Waardes')

        if not isinstance(naar, pycom.Knoop):
            naar = pycom.Knoop(naar)

        if ((self.eenheid is None and naar.eenheid is not None)
                or (self.eenheid is not None and naar.eenheid is None)):
            raise ValueError('knopen moeten zelfde type eenheid hebben')
        naar.eenheid = self.eenheid

        if self[-1].tolist() != naar.array.tolist():
            self._array = np.append(self.array, [naar.array.tolist()], axis=0)
        return self

    def lijn_bezier(self, richting, naar, stappen=100):
        """Verlengt lijn object als kwadratische Bezier kromme naar opgegeven knoop. Hierbij worden <aantal stappen> rechte lijnen gemaakt."""
        if not (isinstance(richting, pycom.Knoop)
                or isinstance(richting, list) or isinstance(richting, tuple)):
            raise TypeError('opgegeven richting-knoop is geen Knoop object of lijst met getallen/Waardes')
        if not (isinstance(naar, pycom.Knoop)
                or isinstance(naar, list) or isinstance(naar, tuple)):
            raise TypeError('opgegeven naar-knoop is geen Knoop object of lijst met getallen/Waardes')

        if not isinstance(richting, pycom.Knoop):
            richting = pycom.Knoop(richting)
        if not isinstance(naar, pycom.Knoop):
            naar = pycom.Knoop(naar)

        if ((self.eenheid is None and richting.eenheid is not None)
                or (self.eenheid is not None and richting.eenheid is None)):
            raise ValueError('knopen moeten zelfde type eenheid hebben')
        richting.eenheid = self.eenheid
        if ((self.eenheid is None and naar.eenheid is not None)
                or (self.eenheid is not None and naar.eenheid is None)):
            raise ValueError('knopen moeten zelfde type eenheid hebben')
        naar.eenheid = self.eenheid

        start = pycom.Knoop(self[-1].tolist())
        start.eenheid = self.eenheid

        tt = np.linspace(0, 1, num=stappen+1)
        P1 = start[:]
        P2 = richting[:]
        P3 = naar[:]

        extra_knopen=[]
        for t in tt[1:]:
            # kwadratische Bezier kromme:
            extra_knoop = (1 - t**2)*P1 + 2*t*(1-t)*P2 + t**2*P3
            extra_knopen.append(extra_knoop.tolist())

        self._array = np.append(self.array, extra_knopen, axis=0)
        return self

    def lijn_cirkelboog(self, middelpunt, gradenhoek:float, stappen=100):
        """Verlengt lijn object als cirkel met middelpunt over x aantal graden. Hierbij worden <aantal stappen> rechte lijnen gemaakt. Positief is tegen klok in, negatief is met de klok mee."""
        if not (isinstance(middelpunt, pycom.Knoop)
                or isinstance(middelpunt, list) or isinstance(middelpunt, tuple)):
            raise TypeError('opgegeven middelpunt-knoop is geen Knoop object of lijst met getallen/Waardes')

        if not isinstance(middelpunt, pycom.Knoop):
            middelpunt = pycom.Knoop(middelpunt)

        if ((self.eenheid is None and middelpunt.eenheid is not None)
                or (self.eenheid is not None and middelpunt.eenheid is None)):
            raise ValueError('knopen moeten zelfde type eenheid hebben')
        middelpunt.eenheid = self.eenheid

        start = pycom.Knoop(self[-1].tolist())
        start.eenheid = self.eenheid

        P1 = start[:]
        M = middelpunt[:]
        straal = np.linalg.norm(M - P1)
        hoek = gradenhoek%360 if gradenhoek >= 0 else -1*((-1*gradenhoek)%360)
        hoek = 360 if hoek == 0 else hoek
        start_hoek = (270-np.rad2deg(np.arctan2(M[0]-P1[0], M[1]-P1[1])))%360
        eind_hoek = start_hoek + hoek

        tt = np.linspace(np.deg2rad(start_hoek), np.deg2rad(eind_hoek), num=stappen+1)
        extra_knopen=[]
        for t in tt[1:]:
            extra_knoop = [M[0] + straal*np.cos(t), M[1] + straal*np.sin(t)]
            extra_knopen.append(extra_knoop)

        self._array = np.append(self.array, extra_knopen, axis=0)
        return self

    def plot2d(self):
        """Teken simpele plot van lijn (met 2 dimensies)."""
        plt.plot(self.array[:,0], self.array[:,1])
        plt.axis('equal')
        plt.show()

    def __eq__ (self, andere):
        """Vergelijkt twee Lijn objecten."""
        if len(self) != len(andere):
            return False
        return all(s == a for s, a in zip(self, andere))

    def __neq__ (self, andere):
        """Vergelijkt negatief twee Lijn objecten."""
        return not self == andere

    def __and__(self, andere):
        """Controleert of Lijn zelfde type eenheid heeft als andere."""
        if not isinstance(andere, Lijn):
            raise TypeError('tweede waarde is geen Lijn object')
        Waarde = pycom.Waarde
        return Waarde(1, self.eenheid) & Waarde(1, andere.eenheid)

    def __iter__(self):
        """Itereert over knopen en geeft Knoop objecten terug."""
        for k_array in self.array:
            k = pycom.Knoop(k_array.tolist())
            k.eenheid = self.eenheid
            yield k

    def __getitem__(self, index):
        """Retourneert subset Numpy array object met getallen (zonder eenheid)."""
        return self.array[index]

    def __len__(self):
        """Geeft aantal knopen."""
        return len(self.array)

    def __float__(self):
        """Berekent de totale lengte van de lijnstukken als float object."""
        if len(self) < 2:
            return 0.0
        laatste_kn_arr = self[0]
        lengte = 0.0
        for kn_arr in self[1:]:
            x1 = laatste_kn_arr[0]
            x2 = kn_arr[0]
            y1 = laatste_kn_arr[1]
            y2 = kn_arr[1]
            lengte += np.sqrt((x2-x1)**2 + (y2-y1)**2)
            laatste_kn_arr = kn_arr
        return lengte

    def __abs__(self):
        """Berekent de totale lengte van de lijnstukken als Waarde object."""
        return pycom.Waarde(float(self), self.eenheid)

    def __format__(self, config:str=None):
        """Geeft tekst met geformatteerd getal en eenheid."""
        if config is None:
            return str(self)
        knopen = ', '.join(format(k, config).rsplit(')', 1)[0]+')' for k in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(knopen, eenheid).strip()

    def __repr__(self):
        cls_naam = type(self).__name__
        knopen = ', '.join(repr(k) for k in self)
        return '{}({})'.format(cls_naam, knopen)

    def __str__(self):
        knopen = ', '.join(str(k).rsplit(')', 1)[0]+')' for k in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(knopen, eenheid).strip()
