import math

import numpy as np


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
        """Checkt of lijn l1a-l1b de lijn l2a-l2b kruist of raakt, op de
        lijnstukken TUSSEN de punten en INCLUSIEF de punten zelf."""
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

    @classmethod
    def bereken_traagheidsmomenten_driehoek(cls, p1, p2, p3):
        nc = cls.bereken_zwaartepunt_driehoek(p1, p2, p3)
        ncx = nc[0]
        ncy = nc[1]
        c = [p1, p2, p3]
        Ixx = 0.0
        Iyy = 0.0
        Ixy = 0.0
        l = len(c)
        for i in range(l):
            p = [c[i][0] - ncx, c[i][1] - ncy]
            p_volgende = [c[(i + 1) % l][0] - ncx,
                          c[(i + 1) % l][1] - ncy]
            a = abs(p[0] * p_volgende[1] - p_volgende[0] * p[1])
            Ixx += (p[0] * p[0] + p[0] * p_volgende[0] +
                    p_volgende[0] * p_volgende[0]) * a
            Iyy += (p[1] * p[1] + p[1] * p_volgende[1] +
                    p_volgende[1] * p_volgende[1]) * a
            Ixy += (p[0] * p_volgende[1] + 2 * p[0] * p[1] +
                2 * p_volgende[0] * p_volgende[1] + p_volgende[0] * p[1]) * a
        Ixx /= 12.0
        Iyy /= 12.0
        Ixy /= 24.0
        return [Ixx, Iyy, Ixy]

    @classmethod
    def genereer_net(cls, np_array):
        """Triangulatie van niet-convexe polygoon."""

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
                    if cls.lijn_raakt_lijn(p1, p2, pp1, pp2):
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
                if cls.punt_op_lijn([vorige_x, vorige_y],
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
        coordinaten_met_klok_mee = True
        if volgende_c[0] > vorige_c[0]:
            interpol_y = cls.interpoleer_over_lijn(
                    linker_c, volgende_c, vorige_c[0])
            if interpol_y != 99999:
                volgende_y = interpol_y
        else:
            interpol_y = cls.interpoleer_over_lijn(
                    linker_c, vorige_c, volgende_c[0])
            if interpol_y != 99999:
                vorige_y = interpol_y
        if volgende_y < vorige_y:
            coordinaten_met_klok_mee = False

        # hoek berekenen en toevoegen aan array
        for i in range(l):
            p = coordinaten[i]
            vorige_p = coordinaten[(i - 1 + l) % l]
            volgende_p = coordinaten[(i + 1) % l]
            hoek = cls.bereken_hoek(
                    vorige_p, p, volgende_p,
                    not coordinaten_met_klok_mee)
            coordinaten[i].append(hoek)

        np_array = np.array([[x, y, h] for x, y, _, h in coordinaten])

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
                                if cls.lijn_raakt_lijn(
                                        p_vorige, p_volgende, p_sub,
                                        p_sub_volgende):
                                    over_lijn = True

                        hoek_vorige = cls.bereken_hoek(
                                p_volgende, p_vorige, p,
                                not coordinaten_met_klok_mee)
                        if hoek_vorige > 180:
                            hoek_vorige = 360 - hoek_vorige

                        hoek_volgende = cls.bereken_hoek(
                                p, p_volgende, p_vorige,
                                not coordinaten_met_klok_mee)
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
                           in enumerate(np_array.tolist())]]

        driehoek_iterator(coordinaten)

        driehoeken = [[d[0][2], d[1][2], d[2][2]] for d in driehoeken]

        driehoeken, driehoeken_lijnen_intern = \
            cls.optimaliseer_net(np_array, driehoeken, driehoeken_lijnen_intern)

        return np.array(driehoeken), np.array(driehoeken_lijnen_intern)


    @classmethod
    def optimaliseer_net(cls, np_array, driehoeken, driehoeken_lijnen_intern):
        """Triangulatie van niet-convexe polygoon optimatliseren.

        Deze functie wordt gebruikt aan het einde van 'genereer_net' functie.

        Scherpe hoeken kunnen met floating points tot onnauwkeurigheden leiden.
        Als lijn tussen twee driehoeken (vierhoek) een scherpe hoek oplevert,
        dan lijn flippen en andere hoekpunten in deze vierhoek laten verbinden.
        """

        aantal_iteraties = 0

        def iterator_optimaliseren():
            nonlocal driehoeken
            nonlocal driehoeken_lijnen_intern
            nonlocal aantal_iteraties

            aantal_iteraties += 1
            if aantal_iteraties > 9999:
                raise RecursionError('maximale aantal iteraties bereikt')

            gevonden = False
            for i_intern, lijn_intern in enumerate(driehoeken_lijnen_intern):
                # zoek corresponderende driehoeken
                driehoek1 = None
                driehoek2 = None
                for i_driehoek, driehoek in enumerate(driehoeken):
                    if (lijn_intern[0] in driehoek
                            and lijn_intern[1] in driehoek):
                        if driehoek1 is None:
                            driehoek1 = (int(str(i_driehoek)), driehoek[:])
                        else:
                            driehoek2 = (int(str(i_driehoek)), driehoek[:])
                            break
                if driehoek1 is None or driehoek2 is None:
                    continue
                tmp1 = driehoek1[1][:]
                del tmp1[tmp1.index(lijn_intern[0])]
                del tmp1[tmp1.index(lijn_intern[1])]
                tmp2 = driehoek2[1][:]
                del tmp2[tmp2.index(lijn_intern[0])]
                del tmp2[tmp2.index(lijn_intern[1])]

                # zoek waarden van hoekpunten van vierhoek op
                ip1 = lijn_intern[0]
                ip2 = lijn_intern[1]
                ip3 = tmp1[0]
                ip4 = tmp2[0]
                p1 = np_array[ip1][:2].tolist()
                p2 = np_array[ip2][:2].tolist()
                p3 = np_array[ip3][:2].tolist()
                p4 = np_array[ip4][:2].tolist()

                # check of nieuwe diagonaal wel de oude diagonaal kruist
                #    (anders komt nieuwe diagonaal wellicht buiten Vorm
                if not cls.lijn_raakt_lijn(p1, p2, p3, p4):
                    continue

                # bereken hoeken van diagonalen en check of nieuwe groter zijn
                hoek_bestaand_1 = min(cls.bereken_hoek(p1, p2, p3, True),
                                      cls.bereken_hoek(p1, p2, p3, False))
                hoek_bestaand_2 = min(cls.bereken_hoek(p2, p1, p3, True),
                                      cls.bereken_hoek(p2, p1, p3, False))
                hoek_bestaand_3 = min(cls.bereken_hoek(p1, p2, p4, True),
                                      cls.bereken_hoek(p1, p2, p4, False))
                hoek_bestaand_4 = min(cls.bereken_hoek(p2, p1, p4, True),
                                      cls.bereken_hoek(p2, p1, p4, False))
                hoek_nieuw_1 = min(cls.bereken_hoek(p3, p4, p1, True),
                                         cls.bereken_hoek(p3, p4, p1, False))
                hoek_nieuw_2 = min(cls.bereken_hoek(p4, p3, p1, True),
                                         cls.bereken_hoek(p4, p3, p1, False))
                hoek_nieuw_3 = min(cls.bereken_hoek(p3, p4, p2, True),
                                         cls.bereken_hoek(p3, p4, p2, False))
                hoek_nieuw_4 = min(cls.bereken_hoek(p4, p3, p2, True),
                                         cls.bereken_hoek(p4, p3, p2, False))
                min_hoek_bestaand = min(hoek_bestaand_1, hoek_bestaand_2,
                                        hoek_bestaand_3, hoek_bestaand_4)
                min_hoek_nieuw = min(hoek_nieuw_1, hoek_nieuw_2,
                                     hoek_nieuw_3, hoek_nieuw_4)

                if min_hoek_nieuw > min_hoek_bestaand:
                    gevonden = True
                    # vervang huidige driehoeken
                    tmp_driehoeken = []
                    for i, driehoek in enumerate(driehoeken):
                        if i == driehoek1[0]:
                            tmp_driehoeken.append([ip3, ip4, ip1])
                        elif i == driehoek2[0]:
                            tmp_driehoeken.append([ip3, ip4, ip2])
                        else:
                            tmp_driehoeken.append(driehoek)
                    driehoeken = tmp_driehoeken
                    # vervang huidige interne lijn
                    tmp_lijnen_intern = []
                    for i, lijn in enumerate(driehoeken_lijnen_intern):
                        if i == i_intern:
                            tmp_lijnen_intern.append([ip3, ip4])
                        else:
                            tmp_lijnen_intern.append(lijn)
                    driehoeken_lijnen_intern = tmp_lijnen_intern
                    break

            if gevonden:
                iterator_optimaliseren()

        # start proces
        iterator_optimaliseren()

        return driehoeken, driehoeken_lijnen_intern
