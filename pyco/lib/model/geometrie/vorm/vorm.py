from typing import Union
import math

import numpy as np
import matplotlib.pyplot as plt

import pyco.model as pycom

from pyco.lib.model.geometrie.vorm.vorm_functies import VormFuncties


class Vorm(pycom.BasisObject):
    """Betreft een meetkundig 2D vorm met bijbehorende eigenschappen.

    AANMAKEN VORM
        v1 = Vorm(Lijn)                 invoeren van één Lijn object
        v2 = Vorm([(0,0),(1,1),(1,0)])  direct invoeren knoopcoordinaten

    EENHEID
        v.eenheid       opvragen huidige eenheid; of None als alleen getal
        v.eenheid = 'm' alle waarden in alle knoopobjecten naar 'm'
        v.gebruik_eenheid('m')   zelfde als bovenstaande, retourneert object

    EIGENSCHAPPEN       naam + '_'  -->  Waarde object i.p.v. getal
        v.O             omtrek   (bijv. v.O_ geeft omtrek Waarde met eenheid)
        v.A             oppervlakte
        v.xmin v.xmax   minimum en maximum x-waarde
        v.ymin v.ymax   minimum en maximum y-waarde
        v.ncx  v.nvy    x- en y-waarde normaalkrachtencetrum (zwaartepunt)
        v.Ixx  v.Iyy    oppervlakte traagheidsmoment in x- en y-richting
        v.Ixy           traagheidsproduct (is 0 voor symmetrische vormen)
        v.I1   v.I2     hoofdtraagheidsmomenten (1 sterke richting, 2 zwakke)
        v.alpha         hoek (tegen klok in) hoofdtraagheidsassen
        v.Wxmin v.Wxmax weerstandsmoment voor vezel x-minimaal en x-maximaal
        v.Wymin v.Wymax weerstandsmoment voor vezel y-minimaal en y-maximaal
        v.kxmin v.kxmax laagste/hoogste x-waarde van kern
        v.kymin v.kymax laagste/hoogste y-waarde van kern

    KNOOP COORDINATEN
        v.array                 Numpy array met x/y coordinaten
        v.array_gesloten        zelfde, met kopie 1e knoop aan het einde
        v.kern_array            Numpy array met x/y coordinaten van kern
        v.kern_array_gesloten   zelfde, met kopie 1e knoop aan het einde

    LIJN OBJECT
        v.lijn        genereert een Lijn object van vorm omtrek (gesloten)

    BEWERKINGEN
        v[3]          subset Numpy array object met getallen (zonder eenheid)
        len(v)        aantal knopen
        for k in v:   itereert over knopen, geeft Knoop object (met eenheid)

    OVERIG
        v.plot()                Matplotlib plot met vormeigenschappen
        v.print_eigenschappen() print overzicht van eigenschappen
        v.print_eigenschappen(knopen=True)  zelfde, met lijst van knopen
    """

    fn = VormFuncties()

    EIGENSCHAPPEN = ('O A xmin xmax ymin ymax ncx ncy Ixx Iyy Ixy I1 I2 '
                     'alpha Wxmin Wxmax Wymin Wymax kxmin kxmax kymin kymax '
                     ).split()

    AFRONDEN_NAAR_NUL = 1e-13

    def __init__(self, lijn:Union[pycom.Lijn, list, tuple]):
        super().__init__()

        if not isinstance(lijn, pycom.Lijn):
            lijn = pycom.Lijn(*lijn)

        self._eenheid = lijn.eenheid

        # controleer knoop data en maak Numpy array
        self._array = self._check_knopen(lijn.array.copy())

        # aanmaken vorm eigenschappen
        # normaal een float object, met underscore erachter een Waarde object
        self.O = None       # omtrek
        self.O_ = None
        self.A = None       # oppervlakte
        self.A_ = None
        self.xmin = None    # laagste x-waarde (links)
        self.xmin_ = None
        self.xmax = None    # hoogste x-waarde (rechts)
        self.xmax_ = None
        self.ymin = None    # laagste y-waarde (onder)
        self.ymin_ = None
        self.ymax = None    # hoogste y-waarde (boven)
        self.ymax_ = None
        self.ncx = None     # normaalkrachtcentrum x (zwaartepunt horizontaal)
        self.ncx_ = None
        self.ncy = None     # normaalkrachtcentrum y (zwaartepunt verticaal)
        self.ncy_ = None
        self.Ixx = None     # traagheidsmoment xx (buiging belasting x-richting)
        self.Ixx_ = None
        self.Iyy = None     # traagheidsmoment yy (buiging belasting y-richting)
        self.Iyy_ = None
        self.Ixy = None     # wringtraagheidsmoment xy
        self.Ixy_ = None
        self.I1 = None      # hoofdtraagheidsmoment 1 (sterke as)
        self.I1_ = None
        self.I2 = None      # hoofdtraagheidsmoment 2 (zwakke as)
        self.I1_ = None
        self.alpha = None   # hoek van hoofdtraagheidsassen in graden
        self.alpha_ = None
        self.Wxmin = None   # weerstandsmoment t.p.v. laagste x-waarde (links)
        self.Wxmin_ = None
        self.Wxmax = None   # weerstandsmoment t.p.v. hoogste x-waarde (rechts)
        self.Wxmax_ = None
        self.Wymin = None   # weerstandsmoment t.p.v. laagste y-waarde (onder)
        self.Wymin_ = None
        self.Wymax = None   # weerstandsmoment t.p.v. hoogste y-waarde (boven)
        self.Wymax_ = None
        self.kxmin = None   # laagste x-waarde kern (links)
        self.kxmin_ = None
        self.kxmax = None   # hoogste x-waarde kern (rechts)
        self.kxmax_ = None
        self.kymin = None   # laagste y-waarde kern (onder)
        self.kymin_ = None
        self.kymax = None   # hoogste y-waarde kern (boven)
        self.kymax_ = None

        self._bereken_eigenschappen()
        self._bereken_waardes()

        self._kern_array = np.array([])  # xy coordinaten van kern
        self._bereken_kern_array()

    def _check_knopen(self, np_array):
        """Checkt knopen en berekent hoeken."""

        coordinaten = []
        coordinaten_links_rechts = []

        # zorgen dat laatste knoop niet zelfde is als eerste
        if np_array[0].tolist() == np_array[-1].tolist():
            np_array = np.delete(np_array, (-1), axis=0)

        # zorgen dat omtrek lijnen elkaar nergens kruisen/raken
        l = len(np_array)
        for i in range(l):
            # kies een lijn
            p1 = [np_array[i][0], np_array[i][1]]
            p2 = [np_array[(i+1)%l][0], np_array[(i+1)%l][1]]
            for ii in range(i, l):
                # check alle andere lijnen
                if i != (ii-1)%l and i != ii and i != (ii+1)%l:
                    pp1 = [np_array[ii][0], np_array[ii][1]]
                    pp2 = [np_array[(ii+1)%l][0], np_array[(ii+1)%l][1]]
                    if self.fn.lijn_raakt_lijn(p1, p2, pp1, pp2):
                        raise ValueError('Omtrek van vorm mag zichzelf nergens raken/kruisen. Volgende lijnen doen dat wel: Lijn({}, {}) & Lijn({}, {})'.format(p1, p2, pp1, pp2))

        def verwijder_punt_op_lijn(c):
            nonlocal coordinaten_links_rechts
            punt_op_lijn_gevonden = False
            c = c if (isinstance(c, list) or isinstance(c, tuple)) else []
            n = len(c)

            for i in range(n):
                x = c[i][0]
                y = c[i][1]
                vorige_x = c[(i - 1 + n) % n][0]
                vorige_y = c[(i - 1 + n) % n][1]
                volgende_x = c[(i + 1) % n][0]
                volgende_y = c[(i + 1) % n][1]
                if self.fn.punt_op_lijn([vorige_x, vorige_y],
                                        [volgende_x, volgende_y], [x, y]):
                    del c[i]
                    punt_op_lijn_gevonden = True
                    break
            if punt_op_lijn_gevonden:
                verwijder_punt_op_lijn(c)
            else:
                n = len(c)
                for i in range(n):
                    coordinaten.append([c[i][0], c[i][1], i])
                coordinaten_links_rechts = sorted(
                        coordinaten, key=lambda x: x[0])

        verwijder_punt_op_lijn(np_array.tolist())

        if len(np_array) < 3:
            raise ValueError('Vorm moet minimaal drie knopen bevatten (die niet op één lijn liggen).')

        return np_array

    def _float(self, waarde):
        """Zet object om naar een float en rond hele kleine waarden af naar nul."""
        f = float(waarde)
        if f > -1*self.AFRONDEN_NAAR_NUL and f < 1*self.AFRONDEN_NAAR_NUL:
            f = 0.0
        return f

    def _bereken_eigenschappen(self, alleen_A_O_minmax_nc=False):
        """Berekent alle geometrische eigenschappen."""

        arr = self.array
        Xi = arr[:,0]
        Yi = arr[:,1]
        Xii = np.delete(np.hstack((Xi, np.array([Xi[0]]))), 0)
        Yii = np.delete(np.hstack((Yi, np.array([Yi[0]]))), 0)
        determinant = Xi*Yii - Xii*Yi

        A = 1/2 * sum(determinant)
        if not A:
            return

        # als coordinaten tegen de klok in zijn ingevoerd, dan positief
        # als coordinaten met de klok mee zijn ingevoerd, dan negatief
        teken = 1.0 if A > 0 else -1.0

        self.A = self._float(teken * A)
        self.O = self._float(pycom.Lijn(self.array_gesloten.tolist()))
        self.xmin = self._float(Xi.min())
        self.xmax = self._float(Xi.max())
        self.ymin = self._float(Yi.min())
        self.ymax = self._float(Yi.max())
        self.ncx = self._float(
            teken * 1/6/self.A * sum((Xi + Xii) * determinant))
        self.ncy = self._float(
            teken * 1/6/self.A * sum((Yi + Yii) * determinant))

        if alleen_A_O_minmax_nc:
            return

        # vanaf nu alle coordinaten t.o.v. zwaartepunt relativeren
        Xi_ = Xi - self.ncx
        Yi_ = Yi - self.ncy
        Xii_ = np.delete(np.hstack((Xi_, np.array([Xi_[0]]))), 0)
        Yii_ = np.delete(np.hstack((Yi_, np.array([Yi_[0]]))), 0)
        determinant_ = Xi_*Yii_ - Xii_*Yi_

        self.Ixx = self._float(
            teken * 1/12 * sum((Xi_**2 + Xi_*Xii_ + Xii_**2) * determinant_))
        self.Iyy = self._float(
            teken * 1/12 * sum((Yi_**2 + Yi_*Yii_ + Yii_**2) * determinant_))
        self.Ixy = self._float(
            teken * 1/24 * sum((Xi_*Yii_ + 2*Xi_*Yi_ + 2*Xii_*Yii_ + Xii_*Yi_) * determinant_))

        self.Wxmin = self._float(self.Ixx / abs(self.ncx - self.xmin))
        self.Wxmax = self._float(self.Ixx / abs(self.ncx - self.xmax))
        self.Wymin = self._float(self.Iyy / abs(self.ncx - self.xmin))
        self.Wymax = self._float(self.Iyy / abs(self.ncx - self.xmax))
        self.kxmin = self._float(-1 * self.Wxmax / self.A)
        self.kxmax = self._float(self.Wxmin / self.A)
        self.kymin = self._float(-1 * self.Wxmax / self.A)
        self.kymax = self._float(self.Wxmin / self.A)
        self.I1 = self._float((self.Ixx + self.Iyy) / 2
                   + np.sqrt((self.Ixx - self.Iyy)**2 + 4*self.Ixy**2)/2)
        self.I2 = self._float((self.Ixx + self.Iyy) / 2
                   - np.sqrt((self.Ixx - self.Iyy)**2 + 4*self.Ixy**2)/2)
        if self.Ixx - self.Iyy != 0:  # kan niet delen door 0
            self.alpha = self._float((math.atan(2 * self.Ixy /
                (self.Ixx - self.Iyy))/2) * (360 / (2 * math.pi)))
        elif self.Ixy == 0: # hor/vert symmetrisch: bijvoorbeeld rechthoek
            self.alpha = 0.0
        else: # Ixx == Iyy, maar niet hor/vert symmetrisch: bijvoorbeeld ruit
            self.alpha = 45.0

    def _bereken_waardes(self):
        # maak Waarde objecten met eenheid
        oppervlakte_eenheid = None
        weerstand_eenheid = None
        traagheid_eenheid = None
        if self.eenheid is not None:
            oppervlakte_eenheid = '{}2'.format(self.eenheid)
            weerstand_eenheid = '{}3'.format(self.eenheid)
            traagheid_eenheid = '{}4'.format(self.eenheid)
        self.O_ = pycom.Waarde(self.O, self.eenheid)
        self.A_ = pycom.Waarde(self.A, oppervlakte_eenheid)
        self.xmin_ = pycom.Waarde(self.xmin, self.eenheid)
        self.xmax_ = pycom.Waarde(self.xmax, self.eenheid)
        self.ymin_ = pycom.Waarde(self.ymin, self.eenheid)
        self.ymax_ = pycom.Waarde(self.ymax, self.eenheid)
        self.ncx_ = pycom.Waarde(self.ncx, self.eenheid)
        self.ncy_ = pycom.Waarde(self.ncy, self.eenheid)
        self.Ixx_ = pycom.Waarde(self.Ixx, traagheid_eenheid)
        self.Iyy_ = pycom.Waarde(self.Iyy, traagheid_eenheid)
        self.Ixy_ = pycom.Waarde(self.Ixy, traagheid_eenheid)
        self.I1_ = pycom.Waarde(self.I1, traagheid_eenheid)
        self.I2_ = pycom.Waarde(self.I2, traagheid_eenheid)
        self.alpha_ = pycom.Waarde(self.alpha, 'deg')
        self.Wxmin_ = pycom.Waarde(self.Wxmin, weerstand_eenheid)
        self.Wxmax_ = pycom.Waarde(self.Wxmax, weerstand_eenheid)
        self.Wymin_ = pycom.Waarde(self.Wymin, weerstand_eenheid)
        self.Wymax_ = pycom.Waarde(self.Wymax, weerstand_eenheid)
        self.kxmin_ = pycom.Waarde(self.kxmin, self.eenheid)
        self.kxmax_ = pycom.Waarde(self.kxmax, self.eenheid)
        self.kymin_ = pycom.Waarde(self.kymin, self.eenheid)
        self.kymax_ = pycom.Waarde(self.kymax, self.eenheid)

    def _bereken_kern_array(self):
        """Berekent het gebied daar waar een normaaldrukkracht NIET in trekspanningen resulteert."""
        kernpunten = [] # lijst met xy coordinaten van kern
        elastiek_lijn = [] # lijst met xy coordinaten als elastiek om vorm

        def bereken_geroteerde_coordinaten(p, alpha, z):
            alpha = -alpha
            xrot = (1.0 * math.cos(alpha * (2 * math.pi / 360)) *
                    (p[0] - z[0]) + math.sin(alpha * (2 * math.pi / 360)) *
                    (p[1] - z[1]))
            yrot = (-1.0 * math.sin(alpha * (2 * math.pi / 360)) *
                    (p[0] - z[0]) + math.cos(alpha * (2 * math.pi / 360)) *
                    (p[1] - z[1]))
            return [xrot + z[0], yrot + z[1]]

        def maak_groot_getal(x):
            return math.floor(x * 1e12)

        c = self.array.tolist()
        l = len(c)
        p = [c[0][0], c[0][1]]

        for i in range(l):
            geldig = True
            p_volgende = [c[(i + 1) % l][0], c[(i + 1) % l][1]]
            test_lijn = [p.copy(), p_volgende.copy()]
            if test_lijn[0][0] == test_lijn[1][0]: # verticale lijn
                if (test_lijn[0][0] < self.xmax
                        and test_lijn[0][0] > self.xmin):
                    geldig = False
            else: # horizontaal of diagonaal
                a = (1.0 * (test_lijn[1][1] - test_lijn[0][1]) /
                    (test_lijn[1][0] - test_lijn[0][0]))
                b = 1.0 * test_lijn[0][1] - test_lijn[0][0] * a
                is_hoger = False
                is_lager = False
                for ii in range(l):
                    if (maak_groot_getal(c[ii][1])
                            > maak_groot_getal(a * c[ii][0] + b) + 10):
                        is_hoger = True
                    elif (maak_groot_getal(c[ii][1])
                            < maak_groot_getal(a * c[ii][0] + b) - 10):
                        is_lager = True
                if is_hoger and is_lager:
                    geldig = False
            if geldig:
                elastiek_lijn.append([p.copy(), p_volgende.copy()])
                p = [c[(i + 1) % l][0], c[(i + 1) % l][1]]

        ncx = self.ncx
        ncy = self.ncy
        n = len(elastiek_lijn)
        for i in range(n):
            rand_lijn = elastiek_lijn[i]
            lijn = [[rand_lijn[0][0] - ncx, rand_lijn[0][1] - ncy],
                    [rand_lijn[1][0] - ncx, rand_lijn[1][1] - ncy]]
            inverse_x1 = 0
            inverse_y1 = 0
            if lijn[0][0] == lijn[1][0]: # verticale lijn
                if lijn[0][0] == 0:
                    inverse_x1 = 99e99
                else:
                    inverse_x1 = 1 / lijn[0][0]
                inverse_y1 = 0
            elif lijn[0][1] == lijn[1][1]: # horizontale lijn
                inverse_x1 = 0
                if lijn[0][1] == 0:
                    inverse_y1 = 99e99
                else:
                    inverse_y1 = 1/ lijn[0][1]
            else: # diagonale lijn
                lijn = sorted(lijn, key=lambda x: x[0]) # sorteer op x-waarde
                a = (1.0 * (lijn[1][1] - lijn[0][1])
                     / (lijn[1][0] - lijn[0][0]))
                b = 1.0 * lijn[0][1] - lijn[0][0] * a
                if a == 0 or b == 0:
                    inverse_x1 = 99e99
                else:
                    inverse_x1 = 1/ (-1 * b / a)
                if b == 0:
                    inverse_y1 = 99e99
                else:
                    inverse_y1 = 1 / b
            ex = (-1.0 / self.A * (self.Ixx * inverse_x1
                                   + self.Ixy * inverse_y1))
            ey = (-1.0 / self.A * (self.Ixy * inverse_x1
                                   + self.Iyy * inverse_y1))
            kernpunten.append([ex + ncx, ey + ncy])

        self._kern_array = np.array(kernpunten)

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
            k = pycom.Knoop(k_array.tolist())
            k.eenheid = oude_eenheid
            k.eenheid = eenheid
            tmp_knopen.append(k.array.tolist())

        self._array = self._check_knopen(np.array(tmp_knopen, dtype='float64'))
        self._eenheid = eenheid

        self._bereken_eigenschappen()
        self._bereken_waardes()
        self._bereken_kern_array()

    def gebruik_eenheid(self, eenheid:str):
        """Zet knopen om naar nieuwe eenheid en retourneert object."""
        self.eenheid = eenheid
        return self

    @property
    def array(self) -> np.array:
        """Retourneert Numpy array object met alle getallen (zonder eenheid)."""
        return self._array

    @property
    def array_gesloten(self) -> np.array:
        """Retourneert Numpy array object met alle getallen (zonder eenheid) waarbij startpunt OOK als laatste punt wordt aangehouden."""
        if len(self.array) > 0:
            return np.append(self.array, [self[0].tolist()], axis=0)
        else:
            return np.array([])

    @property
    def kern_array(self) -> np.array:
        """Retourneert Numpy array object met alle knopen van kern (zonder eenheid)."""
        return self._kern_array

    @property
    def kern_array_gesloten(self) -> np.array:
        """Retourneert Numpy array object met allen knopen van kern (zonder eenheid) waarbij startpunt OOK als laatste punt wordt aangehouden."""
        if len(self.kern_array) > 0:
            return np.append(self.kern_array,
                         [self.kern_array[0].tolist()], axis=0)
        else:
            return np.array([])

    @property
    def lijn(self) -> pycom.Lijn:
        """Retourneert Lijn object dat correspondeert met (gesloten) Vorm."""
        knoop_objecten = [k for k in self]
        return pycom.Lijn(knoop_objecten + [knoop_objecten[0]])

    def plot(self):
        """Teken vorm."""
        plt.axis('equal')

        # omtrek vorm
        if len(self.array > 2):
            X = self.array_gesloten[:,0]
            Y = self.array_gesloten[:,1]
            plt.fill(X, Y, 'r', alpha=0.2)
            plt.plot(X, Y, 'r-', lw=2)

        # kern vorm
        if len(self.kern_array > 2):
            X = self.kern_array_gesloten[:,0]
            Y = self.kern_array_gesloten[:,1]
            plt.fill(X, Y, 'b', alpha=0.2)
            plt.plot(X, Y, 'b-', lw=1)

        # hoofdtraagsheidsassens
        marge = 0.1
        hoek = self.alpha / 180 * math.pi
        ymin = self.ymin - (self.ymax - self.ymin) * marge
        ymax = self.ymax + (self.ymax - self.ymin) * marge
        xmin = self.xmin - (self.xmax - self.xmin) * marge
        xmax = self.xmax + (self.xmax - self.xmin) * marge
        x_ymin = self.ncx + (self.ncy - ymin) * math.tan(hoek)
        x_ymax = self.ncx - (ymax - self.ncy) * math.tan(hoek)
        y_xmin = self.ncy - (self.ncx - xmin) * math.tan(hoek)
        y_xmax = self.ncy + (xmax - self.ncx) * math.tan(hoek)
        plt.plot([x_ymin, x_ymax], [ymin, ymax], 'g-', lw=1)
        plt.plot([xmin, xmax], [y_xmin, y_xmax], 'g-', lw=1)

        # zwaartepunt
        plt.plot(self.ncx, self.ncy, 'bo')

        plt.show()

    def print_eigenschappen(self, knopen=False):
        print_queue = []

        if knopen:
            print_queue.append(
                    'knopen (afgerond op 2 decimalen):\n{} {}'.format(
                    [(round(k[0], 2), round(k[1], 2)) for k in self.array],
                    self.eenheid if self.eenheid is not None else '').strip())

            print_queue.append('')

        print_queue.append('\n'.join(['{:>8} = {:.3f}'.format(
                a, getattr(self, a+'_')) for a in self.EIGENSCHAPPEN]))

        print('\n{}\n'.format('\n'.join(print_queue)))

    def __getitem__(self, index) -> np.array:
        """Retourneert subset Numpy array object met getallen (zonder eenheid)."""
        return self.array[index]

    def __len__(self):
        """Geeft aantal knopen."""
        return len(self.array)

    def __iter__(self):
        """Itereert over knopen en geeft Knoop objecten terug."""
        for k_array in self.array:
            k = pycom.Knoop(k_array.tolist())
            k.eenheid = self.eenheid
            yield k

    def __repr__(self):
        cls_naam = type(self).__name__
        knopen = ', '.join(repr(k) for k in self)
        return '{}(Lijn({}))'.format(cls_naam, knopen)

    def __str__(self):
        return '{} {}'.format(
                # coordinaten afgerond op twee decimalen
                [(round(k[0], 2), round(k[1], 2)) for k in self.array],
                self.eenheid if self.eenheid is not None else '').strip()


if __name__ == '__main__':

    v1 = Vorm(pycom.Lijn(
            (4, -5), (-10, 10)
        ).lijn_cirkelboog(
            middelpunt=(0,0),
            gradenhoek=+220
        ).lijn_recht(
            naar=(4, 10)
        ).lijn_bezier(
            richting=(-10,-4),
            naar=(4, -5)
        ).transformeren(
            rotatiehoek=30,
            translatie=[15, 5],
        ))
    v1.plot()
    v1.print_eigenschappen()

    v2 = Vorm([[0,0], [0,10], [4,10], [4,7], [6,7], [6,10], [10,10], [10,0]])
    v2.plot()
    v2.print_eigenschappen()

    v3= Vorm(pycom.Lijn([-1,0]).lijn_cirkelboog(middelpunt=(0,0), gradenhoek=360))
    v3.plot()
    v3.print_eigenschappen()

    v4 = Vorm(pycom.Lijn([0,0], [6,-3], [10,4]).gebruik_eenheid('cm'))
    v4.plot()
    v4.print_eigenschappen()

    v5 = Vorm(pycom.Lijn([-50,-20], [50,-20], [50,20], [-50, 20]).transformeren(
              rotatiepunt=None, # bij None: neemt zwaartepunt
              rotatiehoek=0, # graden tegen de klok in
              schaalfactor=[1, 1], # vergroten om rotatiepunt; negatief:spiegelen
              translatie=[0, 0] # verplaatsing
        ).gebruik_eenheid('mm'))
    v5.plot()
    v5.print_eigenschappen()

    v6 = Vorm(pycom.Lijn([2,0], [0,2], [8,10], [10, 8]).gebruik_eenheid('cm'))
    v6.plot()
    v6.print_eigenschappen()

    v7 = pycom.Rechthoek(breedte=30, hoogte=50)
    v7.plot()
    v7.print_eigenschappen()

    v8 = pycom.Cirkel(straal=pycom.Waarde(1).dm).gebruik_eenheid('m')
    v8.plot()
    v8.print_eigenschappen()
