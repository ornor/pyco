from typing import Union
import math

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

    @classmethod
    def bereken_hoek(cls, p1, p2, p3, clockw=False):
        """Berekent de hoek in graden tussen punten p1, p2 en p3."""
        det = ((p2[0] - p1[0]) * (p3[1] - p1[1])
                   - (p2[1] - p1[1]) * (p3[0] - p1[0]))
        vec1 = [p2[0] - p1[0], p2[1] - p1[1]]
        vec2 = [p3[0] - p2[0], p3[1] - p2[1]]
        product = vec1[0] * vec2[0] + vec1[1] * vec2[1]

        factor = 0.0
        if det != 0:
            factor = 1.0 * product / det
        length1 = math.sqrt(vec1[0]**2 + vec1[1]**2)
        length2 = math.sqrt(vec2[0]**2 + vec2[1]**2)
        denominator = length1 * length2

        angle = 90.0
        if denominator != 0:
            angle = ((math.acos(1.0 * product / denominator)) *
                (360.0 / (2 * math.pi)))

        # angle is defined counter clockwise
        if angle == 0 or angle == 90 or angle == 180:   # angle is orthogonal
            if det == 0:                         # vec2 in line with vec1
                if angle == 180:
                    angle = 0               # 0
                else:
                    angle = 180             # 180
            else:                                # vec2 is not in line with vec1
                if det < 0:                      # p3 is right of vec1
                    angle = 90              # 90
                else:                            # p3 is left of vec1
                    angle = 270             # 270
        else:                                    # angle is not orthogonal
            if det < 0:                          # p3 is right of vec1
                if factor < 0:                   # p3 is further than vec1
                    angle = 180 - angle     # 90-180
                else:                            # p3 is backwards of vec1
                    angle = 180 - angle     # 0-90
            else:                                # p3 is left of vec1
                if factor > 0:                   # p3 is further than vec1
                    angle = 180 + angle     # 180-270
                else:                            # p3 is backwards of vec1
                    angle = 180 + angle     # 270-360
        if clockw:
            angle = (360 - angle) % 360
        return angle

    @classmethod
    def interpoleer_over_lijn(cls, p1, p2, x):
        """Berekent de y-waarde (bij een gegeven x-waarde) over lijn door p1 en p2. Als er geen waarde bepaald kan worden dan: 99999."""
        if p2[0] - p1[0] == 0 or not (
                isinstance(x, int) or isinstance(x, float)):
            return 99999
        else:
            a = 1.0 * (p2[1] - p1[1]) / (p2[0] - p1[0])
            b = 1.0 * p1[1] - p1[0] * a
            return a * x + b

    @classmethod
    def bereken_oppervlakte_driehoek(cls, p1, p2, p3):
        A = (p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) +
            p3[0] * (p1[1] - p2[1])) / 2.0
        return abs(A)

    @classmethod
    def bereken_zwaartepunt_driehoek(cls, p1, p2, p3):
        ncx = (p1[0] + p2[0] + p3[0]) / 3.0
        ncy = (p1[1] + p2[1] + p3[1]) / 3.0
        return [ncx, ncy]


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

        # bij check knopen wordt bepaald welke richting knopen zijn ingevoerd
        self._coordinaten_met_klok_mee = None

        # controleer knoop data en maak Numpy array
        self._array = self._check_knopen(lijn.array.copy())

        # maak net van driehoeken; lijsten verwijzen naar index knoop in array
        self._driehoeken, self._driehoeken_lijnen_intern = self._genereer_net()

        # corrigeer coordinaten in array n.a.v. transformeren vorm
        self.transformeren(translatie,
                           rotatie, rotatiepunt,
                           schaal, schaalpunt)

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
            for ii in range(l):
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

        # uitzoeken of vorm met klok mee gaat of tegen klok in
        linker_c = coordinaten_links_rechts[0]
        l = len(coordinaten)
        volgende_c = coordinaten[(linker_c[2] + 1) % l]
        vorige_c = coordinaten[(linker_c[2] - 1 + l) % l]
        volgende_y = volgende_c[1]
        vorige_y = vorige_c[1]
        self._coordinaten_met_klok_mee = True
        if volgende_c[0] > vorige_c[0]:
            interpol_y = self.fn.interpoleer_over_lijn(
                    linker_c, volgende_c, vorige_c[0])
            if interpol_y != 99999:
                volgende_y = interpol_y
        else:
            interpol_y = self.fn.interpoleer_over_lijn(
                    linker_c, vorige_c, volgende_c[0])
            if interpol_y != 99999:
                vorige_y = interpol_y
        if volgende_y < vorige_y:
            self._coordinaten_met_klok_mee = False

        # hoek berekenen en toevoegen aan array
        for i in range(l):
            p = coordinaten[i]
            vorige_p = coordinaten[(i - 1 + l) % l]
            volgende_p = coordinaten[(i + 1) % l]
            hoek = self.fn.bereken_hoek(
                    vorige_p, p, volgende_p,
                    not self._coordinaten_met_klok_mee)
            coordinaten[i].append(hoek)

        np_array = np.array([[x, y, h] for x, y, _, h in coordinaten])

        if len(np_array) < 3:
            raise ValueError('Vorm moet minimaal drie knopen bevatten (die niet op één lijn liggen).')

        return np_array

    def _genereer_net(self):
        """Triangulatie van niet-convexe polygoon."""
        driehoeken = []
        driehoeken_lijnen_intern = []

        aantal_iteraties = 0

        def driehoek_iterator(polys):
            nonlocal driehoeken
            nonlocal driehoeken_lijnen_intern
            nonlocal aantal_iteraties

            aantal_iteraties += 1
            if aantal_iteraties > 9999:
                raise RecursionError('maximale aantal iteraties bereikt')

            gevonden = False
            for poly_i, poly in enumerate(polys):
                if gevonden:
                    break
                l = len(poly)
                if l > 3:
                    for i in range(l):
                        p = [poly[i][0], poly[i][1],
                            poly[i][2], poly[i][3]] # x,y,i,angle
                        p_vorige = [poly[(i-1+l)%l][0], poly[(i-1+l)%l][1],
                              poly[(i-1+l)%l][2], poly[(i-1+l)%l][3]]
                        p_volgende = [poly[(i+1)%l][0], poly[(i+1)%l][1],
                            poly[(i+1)%l][2], poly[(i+1)%l][3]]
                        over_lijn = False

                        for i_sub in range(l):
                            p_sub = [poly[i_sub][0], poly[i_sub][1],
                                poly[i_sub][2], poly[i_sub][3]]
                            p_sub_volgende = [poly[(i_sub+1)%l][0],
                                poly[(i_sub+1)%l][1],
                                poly[(i_sub+1)%l][2],
                                poly[(i_sub+1)%l][3]]
                            if (not (p_vorige[0] == p_sub[0]
                                    and p_vorige[1] == p_sub[1])
                                and not (p_vorige[0] == p_sub_volgende[0]
                                    and p_vorige[1] == p_sub_volgende[1])
                                and not (p_volgende[0] == p_sub[0]
                                    and p_volgende[1] == p_sub[1])
                                and not (p_volgende[0] == p_sub_volgende[0]
                                    and p_volgende[1] == p_sub_volgende[1])):
                                if self.fn.lijn_raakt_lijn(
                                        p_vorige, p_volgende, p_sub,
                                        p_sub_volgende):
                                    over_lijn = True

                        hoek_vorige = self.fn.bereken_hoek(
                                p_volgende, p_vorige, p,
                                not self._coordinaten_met_klok_mee)
                        if hoek_vorige > 180:
                            hoek_vorige = 360 - hoek_vorige

                        hoek_volgende = self.fn.bereken_hoek(
                                p, p_volgende, p_vorige,
                                not self._coordinaten_met_klok_mee)
                        if hoek_volgende > 180:
                            hoek_volgende = 360 - hoek_volgende

                        if ((not over_lijn) and p[3] < 180
                                and hoek_vorige < p_vorige[3]
                                and hoek_volgende < p_volgende[3]):
                            poly1 = [
                                [p[0], p[1], p[2], p[3]],
                                [p_vorige[0], p_vorige[1],
                                     p_vorige[2], hoek_vorige],
                                [p_volgende[0], p_volgende[1],
                                     p_volgende[2], hoek_volgende]]
                            poly2 = []

                            for i_temp in range(l):
                                p_temp = poly[i_temp]
                                if (not (p[0] == p_temp[0]
                                         and p[1]==p_temp[1])):
                                    if (p_vorige[0] == p_temp[0]
                                             and p_vorige[1] == p_temp[1]):
                                        poly2.append([
                                            p_temp[0],
                                            p_temp[1],
                                            p_temp[2],
                                            (p_temp[3] - hoek_vorige)])
                                    elif (p_volgende[0] == p_temp[0]
                                              and p_volgende[1] == p_temp[1]):
                                        poly2.append([
                                            p_temp[0],
                                            p_temp[1],
                                            p_temp[2],
                                            (p_temp[3] - hoek_volgende)])
                                    else:
                                        poly2.append(p_temp)

                            polys.append(poly1[:])
                            polys.append(poly2[:])
                            driehoeken_lijnen_intern.append([
                                    p_vorige[2], p_volgende[2]])
                            del polys[poly_i]
                            gevonden = True
                            break

                elif l < 3:
                    raise ValueError('opgegeven poly heeft minder dan drie punten')
                else: # l = 3
                    driehoeken.append(poly[:])
                    del polys[poly_i]
                    gevonden = True
                    break

            if gevonden:
                driehoek_iterator(polys)

        coordinaten = [[[x, y, i, h] for i, (x, y, h)
                           in enumerate(self.array.tolist())]]

        driehoek_iterator(coordinaten)

        driehoeken = [[d[0][2], d[1][2], d[2][2]] for d in driehoeken]

        return np.array(driehoeken), np.array(driehoeken_lijnen_intern)

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

        self._array = self._check_knopen(np.array(tmp_knopen, dtype='float64'))
        self._eenheid = eenheid

    @property
    def array(self) -> np.array:
        """Retourneert Numpy array object met alle getallen (zonder eenheid)."""
        return self._array

    @property
    def array_gesloten(self) -> np.array:
        """Retourneert Numpy array object met alle getallen (zonder eenheid) waarbij startpunt OOK als laatste punt wordt aangehouden."""
        return np.append(self.array, [self[0].tolist()], axis=0)

    def transformeren(self,
                      translatie:Vector=None,
                      rotatie:Union[Waarde, float, int]=None,
                      rotatiepunt:Knoop=None,
                      schaal:Union[Waarde, float, int]=None,
                      schaalpunt:Knoop=None):
        """Verplaatst, roteert en/of verschaalt de vorm."""
        pass

    def plot_net(self):
        """Teken net van driehoeken, gebruikt voor berekenen vorm."""
        plt.triplot(self[:,0], self[:,1], self._driehoeken, 'go-', lw=1)
        plt.axis('equal')
        plt.show()

    def plot(self):
        """Teken vorm."""
        plt.plot(self.array_gesloten[:,0], self.array_gesloten[:,1], 'r-', lw=2)
        plt.axis('equal')
        plt.show()

    def __getitem__(self, index):
        """Retourneert subset Numpy array object met getallen (zonder eenheid)."""
        return self.array[index]

    def __len__(self):
        """Geeft aantal knopen."""
        # laatste knoop is zelfde als eerste knoop
        return len(self.array)

    def __iter__(self):
        """Itereert over knopen en geeft Knoop objecten terug."""
        for k_array in self.array:
            k = Knoop(k_array.tolist())
            k.eenheid = self.eenheid
            yield k

    @property
    def A(self) -> float:
        """Berekent oppervlakte en retourneert een float object."""
        opp = []
        l = len(self)

        for i in range(l):
            opp.append(self[i][0] * self[(i+1)%l][1]
                           - self[(i+1)%l][0] * self[i][1])

        opp_totaal = abs(1/2*sum(opp))
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
        l = len(self)

        for i in range(l):
            z1.append((self[i][0] + self[(i+1)%l][0])
                          * (self[i][0] * self[(i+1)%l][1]
                          - self[(i+1)%l][0] * self[i][1]))
            z2.append((self[i][1] + self[(i+1)%l][1])
                          * (self[i][0] * self[(i+1)%l][1]
                          - self[(i+1)%l][0] * self[i][1]))

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
