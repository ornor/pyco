import re
import math
from fractions import Fraction
from typing import Union

import pyco.model as pycom

class Waarde(pycom.BasisComponent):
    """
    Bevat een getal en bijhorende eenheid.

    AANMAKEN WAARDE
        w = Waarde(getal)
        w = Waarde(getal, eenheid_tekst)

    AANPASSEN EENHEID           pas wanneer waarde wordt getoond als tekst
        w = w['N/mm2']          kan voor alle eenheden
        w = w.N_mm2             kan voor een aantal standaard gevallen

    AANPASSEN AFRONDING         pas wanneer waarde wordt getoond als tekst
        w = w[0]                kan voor alle aantallen decimalen
        w = w._0                kan voor 0 t/m 9 decimalen

    OMZETTEN WAARDE NAAR TEKST  resulteert in nieuw string object
        tekst = str(w)          of automatisch met print(w)

    OMZETTEN WAARDE NAAR GETAL  resulteert in nieuw float object
        getal = w('cm')

    MOGELIJKE BEWERKINGEN       resulteert in nieuw Waarde object
        w3 = w1 + w2            waarde optellen bij waarde
        w3 = w1 - w2            waarde aftrekken van waarde
        w3 = w1 * w2            waarde vermenigvuldigen met waarde
        w3 = w1 / w2            waarde delen door waarde
        w2 = n * w1             getal vermenigvuldigen met waarde
        w2 = w1 * n             waarde vermenigvuldigen met getal
        w2 = n / w1             getal delen door waarde
        w2 = w1 / n             waarde delen door getal
        w2 = w1 ** n            waarde tot de macht een getal

    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        w1 == w2                is gelijk aan
        w1 != w2                is niet gelijk aan
        w1 >  w2                is groter dan
        w1 <  w2                is kleiner dan
        w1 >= w2                is groter dan of gelijk aan
        w1 <= w2                is kleiner dan of gelijk aan

    TEKST EENHEID
        gebruik een getal achter naam eenheid voor 'tot de macht'
        gebruik / (maximaal één keer) om teller en noemer te introduceren
        gebruik * om eenheden te combineren (zowel in teller als noemer)
        bijvoorbeeld: "m3*kPa/s4*m"

    STANDAARD EENHEDEN          deze kan je combineren
        dimensieloos            -
        massa                   ag fg pg ng mug mg cg g hg kg Mg Gg Tg Pg Eg
                                ton kton Mton ounce pound kip stone grain
        lengte                  am fm pm nm mum mm cm dm m dam hm km Mm Gm Tm
                                Pm Em in ft yard zeemijl mijl
        tijd                    as(.attos) fs ps ns mus ms cs ds s das hs ks
                                Ms Gs Ts Ps Es min(.minuut) h d j
        temperatuur             C K F  (als temperatuur in teller, samen met
                                andere eenheden, dan niet om te rekenen)
        hoek                    rad deg gon
        kracht                  N kN MN GN TN  (of massa*lengte/tijd^2)
        spanning                Pa kPa MPa GPa TPa  (of kracht/oppervlakte)
        moment                  Nm kNm MNm Nmm kNmm MNmm  (of kracht*lengte)
        oppervlakte             ca a ha  (of lengte^2)
        inhoud                  ml cl dl l dal hl kl gallon pint floz tbs tsp
                                bbl cup  (of lengte^3)

    BESCHIKBARE EIGENSCHAPPEN   voor snel toekennen van eenheid aan waarde
        a ag am attos bbl C ca cg cl cl_d cl_h cl_j cl_min cl_s cm cm2 cm3
        cm3_d cm3_h cm3_j cm3_min cm3_s cm4 cm_d cm_h cm_j cm_min cm_s cs cup
        d dal dam das deg dg dl dl_d dl_h dl_j dl_min dl_s dm dm2 dm3 dm3_d
        dm3_h dm3_j dm3_min dm3_s dm4 dm_d dm_h dm_j dm_min dm_s ds Eg Em Es
        F fg floz fm fs ft g gallon Gg Gm GN gon GPa grain Gs h ha hg hl hm
        hm2 hm3 hs inch K kg kip kl km km2 km3 km3_d km3_h km3_j km3_min km3_s
        km4 km_d km_h km_j km_min km_s kN kNm kNmm kN_m2 kN_mm2 kPa ks kton l
        l_d l_h l_j l_min l_s m m2 m3 m3_d m3_h m3_j m3_min m3_s m4 Mg mg mijl
        minuut ml ml_d ml_h ml_j ml_min ml_s Mm mm mm2 mm3 mm3_d mm3_h mm3_j
        mm3_min mm3_s mm4 mm_d mm_h mm_j mm_min mm_s MN MNm MNmm MN_m2 MN_mm2
        MPa Ms ms Mton mug mum mus m_d m_h m_j m_min m_s N ng Nm nm Nmm ns
        N_m2 N_mm2 ounce Pa Pg pg pint Pm pm pound print_help Ps ps rad s
        stone tbs Tg Tm TN ton TPa Ts tsp yard zeemijl
    """

    # hulp functie om lijst hierboven te gegeneren; hierna nog bepaalde eigenschappen/methodes verwijderen
    # ' '.join(sorted([a for a in dir(Waarde) if a[0] != '_'], key=lambda x:x.upper()))

    # factoren horende bij basiseenheden, om eenheidsbreuk samen te stellen
    # verschillende priemgetallen, zodat product een uniek resultaat geeft
    BASIS = {
        'DIMENSIELOOS': 1,
        'MASSA': 2,
        'LENGTE': 3,
        'TIJD': 5,
        'TEMPERATUUR': 7,
        'HOEK': 11,
    }

    # unieke eenheidsbreuk dit hoort bij basis- en samengestelde eenheden
    TYPE = {
        'DIMENSIELOOS': Fraction(
            BASIS['DIMENSIELOOS']),
        'MASSA': Fraction(
            BASIS['MASSA']),
        'LENGTE': Fraction(
            BASIS['LENGTE']),
        'TIJD': Fraction(
            BASIS['TIJD']),
        'TEMPERATUUR': Fraction(
            BASIS['TEMPERATUUR']),
        'HOEK': Fraction(
            BASIS['HOEK']),
        'KRACHT': Fraction(
            BASIS['MASSA'] * BASIS['LENGTE'],
            BASIS['TIJD'] * BASIS['TIJD']),
        'SPANNING': Fraction(
            BASIS['MASSA'],
            BASIS['TIJD'] * BASIS['TIJD'] * BASIS['LENGTE']),
        'MOMENT': Fraction(
            BASIS['MASSA'] * BASIS['LENGTE'] * BASIS['LENGTE'],
            BASIS['TIJD'] * BASIS['TIJD']),
        'OPPERVLAKTE': Fraction(
            BASIS['LENGTE'] * BASIS['LENGTE']),
        'INHOUD': Fraction(
            BASIS['LENGTE'] * BASIS['LENGTE'] * BASIS['LENGTE']),
    }

    # regexp om in naam van eenheid de letters van cijfers te scheiden
    RE_NAAM_EENHEID = r'^([a-zA-Z\-]+)([0-9]*)$'

    EENHEID = {
        # 'afkorting': (naam, breuk van basiseenheden, weegfactor)

        # bij niet standaard schaalbare eenheden:
        #   (naam, breuk van basiseenheden,
        #       (weegfunctie, weegfunctie-inverse, weegfunctie-noemerfactor))

        # de weegfactor voor standaard waarde van (niet samengestelde)
        #   basiseenheid MOET gelijk zijn aan 1 (een één: integer, geen float)

        #==============   basis eenheden  ===============

        # DIMENSIELOOS
        '-': ('dimensieloos', TYPE['DIMENSIELOOS'], 1), # standaard

        # MASSA
        'ag': ('attogram', TYPE['MASSA'], 1.0e-21),
        'fg': ('femtogram', TYPE['MASSA'], 1.0e-18),
        'pg': ('picogram',  TYPE['MASSA'], 1.0e-15),
        'ng': ('nanogram', TYPE['MASSA'], 1.0e-12),
        'mug': ('mircogram', TYPE['MASSA'], 1.0e-9),
        'mg': ('milligram', TYPE['MASSA'], 1.0e-6),
        'cg': ('centigram', TYPE['MASSA'], 1.0e-5),
        'dg': ('decigram', TYPE['MASSA'], 1.0e-4),
        'g': ('gram', TYPE['MASSA'], 1.0e-3),
        #'dag': ('decagram', TYPE['MASSA'], 1.0e-2),
        'hg': ('hectogram', TYPE['MASSA'], 1.0e-1),
        'kg': ('kilogram', TYPE['MASSA'], 1), # standaard
        'Mg': ('megagram', TYPE['MASSA'], 1.0e3),
        'Gg': ('gigagram', TYPE['MASSA'], 1.0e6),
        'Tg': ('teragram', TYPE['MASSA'], 1.0e9),
        'Pg': ('petagram', TYPE['MASSA'], 1.0e12),
        'Eg': ('exagram', TYPE['MASSA'], 1.0e15),
        'ton': ('ton', TYPE['MASSA'], 1.0e3),
        'kton': ('kiloton', TYPE['MASSA'], 1.0e6),
        'Mton': ('megaton', TYPE['MASSA'], 1.0e9),
        'ounce': ('ounce', TYPE['MASSA'], 0.0283495),
        'pound': ('pound', TYPE['MASSA'], 0.453592),
        'kip': ('kilopound', TYPE['MASSA'], 453.592),
        'stone': ('stone', TYPE['MASSA'], 6.35029),
        'grain': ('grain', TYPE['MASSA'], 0.0000647989),

        # LENGTE
        'am': ('attometer', TYPE['LENGTE'], 1.0e-18),
        'fm': ('femtometer', TYPE['LENGTE'], 1.0e-15),
        'pm': ('picometer', TYPE['LENGTE'], 1.0e-12),
        'nm': ('nanometer', TYPE['LENGTE'], 1.0e-9),
        'mum': ('micrometer', TYPE['LENGTE'], 1.0e-6),
        'mm': ('millimeter', TYPE['LENGTE'], 1.0e-3),
        'cm': ('centimeter', TYPE['LENGTE'], 1.0e-2),
        'dm': ('decimeter', TYPE['LENGTE'], 1.0e-1),
        'm': ('meter', TYPE['LENGTE'], 1),  # standaard
        'dam': ('decameter', TYPE['LENGTE'], 1.0e1),
        'hm': ('hectometer', TYPE['LENGTE'], 1.0e2),
        'km': ('kilometer', TYPE['LENGTE'], 1.0e3),
        'Mm': ('megameter', TYPE['LENGTE'], 1.0e6),
        'Gm': ('gigameter', TYPE['LENGTE'], 1.0e9),
        'Tm': ('terameter', TYPE['LENGTE'], 1.0e12),
        'Pm': ('petameter', TYPE['LENGTE'], 1.0e15),
        'Em': ('exameter', TYPE['LENGTE'], 1.0e18),
        'in': ('inch (Waarde.inch)', TYPE['LENGTE'], 0.0254000), # eigenschap 'in' niet mogelijk -> 'inch'
        'ft': ('feet', TYPE['LENGTE'], 0.304800),
        'yard': ('yard', TYPE['LENGTE'], 0.914400),
        'zeemijl': ('zeemijl', TYPE['LENGTE'], 1852.00),
        'mijl': ('mijl', TYPE['LENGTE'], 1609.34),

        # TIJD
        'as': ('attoseconde (Waarde.attos)', TYPE['TIJD'], 1.0e-18), # eigenschap 'as' niet mogelijk -> 'attos'
        'fs': ('femtoseconde', TYPE['TIJD'], 1.0e-15),
        'ps': ('picoseconde', TYPE['TIJD'], 1.0e-12),
        'ns': ('nanoseconde', TYPE['TIJD'], 1.0e-9),
        'mus': ('microseconde', TYPE['TIJD'], 1.0e-6),
        'ms': ('milliseconde', TYPE['TIJD'], 1.0e-3),
        'cs': ('centiseconde', TYPE['TIJD'], 1.0e-2),
        'ds': ('deciseconde', TYPE['TIJD'], 1.0e-1),
        's': ('seconde', TYPE['TIJD'], 1),  # standaard
        'das': ('decaseconde', TYPE['TIJD'], 1.0e1),
        'hs': ('hectoseconde', TYPE['TIJD'], 1.0e2),
        'ks': ('kiloseconde', TYPE['TIJD'], 1.0e3),
        'Ms': ('megaseconde', TYPE['TIJD'], 1.0e6),
        'Gs': ('gigaseconde', TYPE['TIJD'], 1.0e9),
        'Ts': ('teraseconde', TYPE['TIJD'], 1.0e12),
        'Ps': ('petaseconde', TYPE['TIJD'], 1.0e15),
        'Es': ('exaseconde', TYPE['TIJD'], 1.0e18),
        'min': ('minuut (Waarde.minuut)', TYPE['TIJD'], 60), # eigenschap 'min' niet mogelijk -> 'minuut'
        'h': ('uur', TYPE['TIJD'], 3600),
        'd': ('dag', TYPE['TIJD'], 24*3600),
        'j': ('jaar', TYPE['TIJD'], 365*24*3600),

        # TEMPERATUUR
        'C': ('graden Celcius', TYPE['TEMPERATUUR'], 1),  # standaard
        'K': ('graden Kelvin', TYPE['TEMPERATUUR'],
              (lambda K: K - 273,
               lambda C: C + 273,
               1.0)),
        # 1 graad C warmer is 1 graad K warmer
        #   -> als temperatuur in noemer van eenheid
        # als temperatuur in teller (samen met andere eenheden),
        #   dan niet om te rekenen
        'F': ('graden Fahrenheit', TYPE['TEMPERATUUR'],
              (lambda F: 1.8 * F + 32,
               lambda C: (C - 32) / 1.8,
               (1 / 1.8))),
        # 1 graad C warmer is 1.8 graden F warmer
        #   -> als temperatuur in noemer van eenheid
        # als temperatuur in teller (samen met andere eenheden),
        #   dan niet om te rekenen

        # HOEK
        'rad': ('radialen', TYPE['HOEK'], 1),  # standaard
        'deg': ('graden', TYPE['HOEK'], ((2 * math.pi) / 360)),
        'gon': ('gon', TYPE['HOEK'], ((2 * math.pi) / 400)),


        # ==============   samengestelde eenheden  ===============

        # KRACHT  -->  t.o.v. 1 kg*m/s2 (= 1 N)
        'N': ('Newton', TYPE['KRACHT'], 1),
        'kN': ('kiloNewton', TYPE['KRACHT'], 1.0e3),
        'MN': ('megaNewton', TYPE['KRACHT'], 1.0e6),
        'GN': ('gigaNewton', TYPE['KRACHT'], 1.0e9),
        'TN': ('teraNewton', TYPE['KRACHT'], 1.0e12),

        # SPANNING  -->  t.o.v. 1 kg/(m*s2) (= 1 N/m2)
        'Pa': ('Pascal', TYPE['SPANNING'], 1.0),
        'kPa': ('kiloPascal', TYPE['SPANNING'], 1.0e3),
        'MPa': ('megaPascal', TYPE['SPANNING'], 1.0e6),
        'GPa': ('gigaPascal', TYPE['SPANNING'], 1.0e9),
        'TPa': ('teraPascal', TYPE['SPANNING'], 1.0e12),

        # MOMENT  -->  t.o.v. 1 kg*m2/s2 (= 1 N*m)
        'Nm': ('Newton meter', TYPE['MOMENT'], 1.0),
        'kNm': ('kiloNewton meter', TYPE['MOMENT'], 1.0e3),
        'MNm': ('megaNewton meter', TYPE['MOMENT'], 1.0e6),
        'Nmm': ('Newton millimeter', TYPE['MOMENT'], 1.0e-3),
        'kNmm': ('kiloNewton millimeter', TYPE['MOMENT'], 1.0),
        'MNmm': ('megaNewton millimeter', TYPE['MOMENT'], 1.0e3),

        # OPPERVLAKTE  -->  t.o.v. 1 m2
        'ca': ('centiare', TYPE['OPPERVLAKTE'], 1.0),
        'a': ('are', TYPE['OPPERVLAKTE'], 1.0e2),
        'ha': ('hectare', TYPE['OPPERVLAKTE'], 1.0e4),

        # INHOUD  -->  t.o.v. 1 m3
        'ml': ('milliliter', TYPE['INHOUD'], 1.0e-6),
        'cl': ('centiliter', TYPE['INHOUD'], 1.0e-5),
        'dl': ('deciliter', TYPE['INHOUD'], 1.0e-4),
        'l': ('liter', TYPE['INHOUD'], 1.0e-3),
        'dal': ('decaliter', TYPE['INHOUD'], 1.0e-2),
        'hl': ('hectoliter', TYPE['INHOUD'], 1.0e-1),
        'kl': ('kiloliter', TYPE['INHOUD'], 1.0),
        'gallon': ('gallon', TYPE['INHOUD'], 0.00454609),
        'pint': ('pint', TYPE['INHOUD'], 0.00056826125),
        'floz': ('fluid ounce', TYPE['INHOUD'], 1.0e-5),
        'tbs': ('eetlepel (tablespoon)', TYPE['INHOUD'], 1.5e-5),
        'tsp': ('theelepel (teaspoon)', TYPE['INHOUD'], 5.0e-6),
        'bbl': ('olievat (oil barrel)', TYPE['INHOUD'], 0.1589873),
        'cup': ('cup (metrisch)', TYPE['INHOUD'], 0.00025),
    }

    STANDAARD_AANTAL_DECIMALEN = 2

    def __init__(self, waarde: Union[int, float, str] = 0,
                 eenheid: Union[str, Fraction] = None, config:dict = None):
        super().__init__()

        if not (isinstance(waarde, int) or isinstance(waarde, float)):
            if isinstance(waarde, Waarde):
                if eenheid is None:
                    self._init_waarde_object_zonder_eenheid(waarde)
                else:
                    # omzetten van dimensieloze waarde naar een bepaalde eenheid
                    if isinstance(eenheid, Fraction):
                        self._init_waarde_object_eenheidbreuk(waarde, eenheid)
                    else:
                        if eenheid is None or eenheid == '':
                            eenheid = '-'
                        self._init_waarde_object_eenheidtekst(waarde, eenheid)
            else:
                self._init_waarde_tekst(waarde)
        elif isinstance(eenheid, Fraction):
            self._init_waarde_eenheidbreuk(waarde, eenheid)
        elif isinstance(eenheid, str):
            if eenheid is None or eenheid == '':
                eenheid = '-'
            self._init_waarde_eenheidtekst(waarde, eenheid)
        else:
            self._init_waarde_getal(waarde)

        if config is not None and isinstance(config, dict):
            self.config = config

    def _init_waarde_getal(self, waarde: Union[int, float]):
        """Initieert alleen een getal."""
        self.is_getal = True
        self.waarde = float(waarde)
        self.eenheidbreuk = Fraction(1)
        self.config = {
            'standaard_eenheid': None,
            'aantal_decimalen': self.STANDAARD_AANTAL_DECIMALEN,
        }

    def _init_waarde_eenheidtekst(self, waarde: Union[int, float], eenheid: str):
        """Initieert een eenheid met tekst."""
        self.is_getal = True
        self.decimalen = self.STANDAARD_AANTAL_DECIMALEN
        self.waarde, self.eenheidbreuk = self._bereken_nieuwe_waarde(eenheid, float(waarde))
        self.config = {
            'standaard_eenheid': eenheid if isinstance(eenheid, str) else '-',
            'aantal_decimalen': self.STANDAARD_AANTAL_DECIMALEN,
        }

    def _init_waarde_eenheidbreuk(self, waarde: Union[int, float], eenheid: Fraction):
        """Initieert een eenheid met Fraction breuk object."""
        self.is_getal = True
        self.waarde = waarde
        self.eenheidbreuk = eenheid
        self.config = {
            'standaard_eenheid': None,
            'aantal_decimalen': self.STANDAARD_AANTAL_DECIMALEN,
        }

    def _init_waarde_object_eenheidtekst(self, waarde, eenheid: str):
        """Initieert getal met Waarde object en eenheid met tekst."""
        if not isinstance(waarde, Waarde):
            raise TypeError('waarde is niet van type Waarde')
        self.is_getal = True
        self.waarde, self.eenheidbreuk = self._bereken_nieuwe_waarde(eenheid, waarde.waarde)
        self.config = {
            'standaard_eenheid': None,
            'aantal_decimalen': self.STANDAARD_AANTAL_DECIMALEN,
        }

    def _init_waarde_object_eenheidbreuk(self, waarde, eenheid: Fraction):
        """Initieert getal met Waarde object en eenheid met Fraction breuk object."""
        if not isinstance(waarde, Waarde):
            raise TypeError('waarde is niet van type Waarde')
        self.is_getal = True
        self.eenheidbreuk = eenheid
        self.waarde = waarde._export_waarde(self.eenheidnaam)
        self.config = {
            'standaard_eenheid': None,
            'aantal_decimalen': self.STANDAARD_AANTAL_DECIMALEN,
        }

    def _init_waarde_object_zonder_eenheid(self, waarde):
        """Initieert getal met Waarde object zonder eenheid."""
        if not isinstance(waarde, Waarde):
            raise TypeError('waarde is niet van type Waarde')
        self.is_getal = waarde.is_getal
        self.eenheidbreuk = waarde.eenheidbreuk
        self.waarde = waarde.waarde
        self.config = waarde.config

    def _init_waarde_tekst(self, waarde:str):
        self.is_getal = False
        self.waarde = waarde
        self.eenheidbreuk = None
        self.config = {
            'standaard_eenheid': None,
            'aantal_decimalen': None,
        }

    @property
    def eenheidnaam(self):
        """Genereert een naam voor eenheid op basis van eenheidbreuk."""

        def priemBASIS(n):
            i = 2
            BASIS = []
            while i * i <= n:
                if n % i:
                    i += 1
                else:
                    n //= i
                    BASIS.append(i)
            if n > 1:
                BASIS.append(n)
            return tuple(BASIS)

        def verbind_namen(namen):
            nieuwe_namen = []
            vorige_naam = None
            aantal_namen = 0
            for naam in namen:
                if vorige_naam is None:
                    vorige_naam = naam
                    aantal_namen = 1
                else:
                    if naam == vorige_naam:
                        aantal_namen += 1
                    else:
                        if aantal_namen > 1:
                            nieuwe_namen.append(vorige_naam + str(aantal_namen))
                        else:
                            nieuwe_namen.append(vorige_naam)
                        vorige_naam = naam
                        aantal_namen = 1
            if vorige_naam is not None:
                if aantal_namen > 1:
                    nieuwe_namen.append(vorige_naam + str(aantal_namen))
                else:
                    nieuwe_namen.append(vorige_naam)
            return '*'.join(nieuwe_namen)

        if not hasattr(self, 'eenheidbreuk'):
            self.eenheidbreuk = Fraction(1)

        evenredig_BASIS = priemBASIS(self.eenheidbreuk.numerator)  # teller
        omgekeerd_evenredig_BASIS = priemBASIS(self.eenheidbreuk.denominator)  # noemer
        evenredig_namen = []
        omgekeerd_evenredig_namen = []

        for factor in evenredig_BASIS:
            for eh_afk, eh_dict in self.EENHEID.items():
                if Fraction(factor) == eh_dict[1] and eh_dict[2] == 1:
                    evenredig_namen.append(eh_afk)
        for factor in omgekeerd_evenredig_BASIS:
            for eh_afk, eh_dict in self.EENHEID.items():
                if Fraction(factor) == eh_dict[1] and eh_dict[2] == 1:
                    omgekeerd_evenredig_namen.append(eh_afk)
        if evenredig_namen and omgekeerd_evenredig_namen:
            omgekeerd_evenredig_namen_str = verbind_namen(omgekeerd_evenredig_namen)
            if '*' in omgekeerd_evenredig_namen_str:
                return '{}/({})'.format(verbind_namen(evenredig_namen),
                                        omgekeerd_evenredig_namen_str)
            else:
                return '{}/{}'.format(verbind_namen(evenredig_namen), omgekeerd_evenredig_namen_str)
        elif evenredig_namen and not omgekeerd_evenredig_namen:
            return '{}'.format(verbind_namen(evenredig_namen))
        elif not evenredig_namen and omgekeerd_evenredig_namen:
            omgekeerd_evenredig_namen_str = verbind_namen(omgekeerd_evenredig_namen)
            if '*' in omgekeerd_evenredig_namen_str:
                return '1/({})'.format(omgekeerd_evenredig_namen_str)
            else:
                return '1/{}'.format(omgekeerd_evenredig_namen_str)
        elif not evenredig_namen and not omgekeerd_evenredig_namen:
            for eh_afk, eh_dict in self.EENHEID.items():
                if Fraction(self.BASIS['DIMENSIELOOS']) == eh_dict[1] and eh_dict[2] == 1:
                    return eh_afk

    def _bereken_nieuwe_waarde(self, eenheid, invoer_waarde):
        """Genereert een interne waarde (getal) op basis van eenheid en invoerwaarde."""
        waarde = invoer_waarde
        if not isinstance(eenheid, str) or not eenheid:
            raise ValueError('eenheid moet een (niet leeg) stuk tekst zijn')
        eenheidbreuk = Fraction(1)
        breukonderdelen = eenheid.split('/')
        if len(breukonderdelen) > 2:
            raise ValueError('er mag maar één \'/\' in eenheid aanwezig zijn')
        teller = breukonderdelen[0]
        if teller == '1':
            teller = ''
        noemer = breukonderdelen[1].lstrip('(').rstrip(')') if len(breukonderdelen) > 1 else ''
        telleronderdelen = [onderdeel.strip() for onderdeel in teller.split('*')] if teller else []
        noemeronderdelen = [onderdeel.strip() for onderdeel in noemer.split('*')] if noemer else []
        for telleronderdeel in telleronderdelen:
            result = re.search(self.RE_NAAM_EENHEID, telleronderdeel)
            if result is None:
                raise ValueError('telleronderdeel van eenheid heeft ongeldige opmaak: \'{}\''.format(telleronderdeel))
            else:
                eenheid_naam = result.group(1)
                eenheid_aantal = int(result.group(2)) if result.group(2) else 1
                if not eenheid_naam in self.EENHEID:
                    raise ValueError('telleronderdeel van eenheid is onbekend: \'{}\''.format(eenheid_naam))
                for _ in range(eenheid_aantal):
                    weging = self.EENHEID[eenheid_naam][2]
                    if isinstance(weging, float) or isinstance(weging, int):
                        waarde = waarde * weging
                    elif isinstance(weging, tuple) and len(weging) == 3 \
                            and callable(weging[0]) and callable(weging[1]) \
                            and (isinstance(weging[2], float) or isinstance(weging[2], int)):
                        if len(telleronderdelen) > 1 or len(noemeronderdelen) > 0:
                            raise ValueError('de niet standaard schaalbare sub-eenheid \'{}\' kan enkel worden omgerekend in teller als het als enige onderdeel voorkomt in hele eenheid; in de noemer kan deze eenheid wel worden gecombineerd'.format(eenheid_naam))
                        waarde = weging[0](waarde)
                    else:
                        raise ValueError('weging basiseenheid heeft verkeerde syntax')
                    subeenheidfactor = self.EENHEID[eenheid_naam][1]
                    eenheidbreuk = eenheidbreuk * subeenheidfactor
        for noemeronderdeel in noemeronderdelen:
            result = re.search(self.RE_NAAM_EENHEID, noemeronderdeel)
            if result is None:
                raise ValueError('noemeronderdeel van eenheid heeft ongeldige opmaak: \'{}\''.format(noemeronderdeel))
            else:
                eenheid_naam = result.group(1)
                eenheid_aantal = int(result.group(2)) if result.group(2) else 1
                if not eenheid_naam in self.EENHEID:
                    raise ValueError('noemeronderdeel van eenheid is onbekend: \'{}\''.format(eenheid_naam))
                for _ in range(eenheid_aantal):
                    weging = self.EENHEID[eenheid_naam][2]
                    if isinstance(weging, float) or isinstance(weging, int):
                        waarde = waarde / weging
                    elif isinstance(weging, tuple) and len(weging) == 3 \
                            and callable(weging[0]) and callable(weging[1]) \
                            and (isinstance(weging[2], float) or isinstance(weging[2], int)):
                        weging_noemerfactor = weging[2]
                        waarde = waarde / weging_noemerfactor
                    else:
                        raise ValueError('weging basiseenheid heeft verkeerde syntax')
                    subeenheidfactor = self.EENHEID[eenheid_naam][1]
                    eenheidbreuk = eenheidbreuk / subeenheidfactor
        return waarde, eenheidbreuk

    def _bereken_inverse_waarde(self, eenheid, oude_waarde, oude_eenheidbreuk):
        """Genereert een waarde (getal) op basis van een eenheid."""
        waarde = oude_waarde
        if not isinstance(eenheid, str) or not eenheid:
            raise ValueError('eenheid moet een (niet leeg) stuk tekst zijn')
        eenheidbreuk = Fraction(1)
        breukonderdelen = eenheid.split('/')
        if len(breukonderdelen) > 2:
            raise ValueError('er mag maar één \'/\' in eenheid aanwezig zijn')
        teller = breukonderdelen[0]
        noemer = breukonderdelen[1].lstrip('(').rstrip(')') if len(breukonderdelen) > 1 else ''
        telleronderdelen = [onderdeel.strip() for onderdeel in teller.split('*')] if teller else []
        noemeronderdelen = [onderdeel.strip() for onderdeel in noemer.split('*')] if noemer else []
        for telleronderdeel in telleronderdelen:
            result = re.search(self.RE_NAAM_EENHEID, telleronderdeel)
            if result is None:
                raise ValueError('telleronderdeel van eenheid heeft ongeldige opmaak: \'{}\''.format(telleronderdeel))
            else:
                eenheid_naam = result.group(1)
                eenheid_aantal = int(result.group(2)) if result.group(2) else 1
                if not eenheid_naam in self.EENHEID:
                    raise ValueError('telleronderdeel van eenheid is onbekend: \'{}\''.format(eenheid_naam))
                for _ in range(eenheid_aantal):
                    weging = self.EENHEID[eenheid_naam][2]
                    if isinstance(weging, float) or isinstance(weging, int):
                        waarde = waarde / weging
                    elif isinstance(weging, tuple) and len(weging) == 3 \
                            and callable(weging[0]) and callable(weging[1]) \
                            and (isinstance(weging[2], float) or isinstance(weging[2], int)):
                        if len(telleronderdelen) > 1 or len(noemeronderdelen) > 0:
                            raise ValueError('de niet standaard schaalbare sub-eenheid \'{}\' kan enkel worden omgerekend in teller als het als enige onderdeel voorkomt in hele eenheid; in de noemer kan deze eenheid wel worden gecombineerd'.format(eenheid_naam))
                        inverse_weging = weging[1]
                        waarde = inverse_weging(waarde)
                    else:
                        raise ValueError('weging basiseenheid heeft verkeerde syntax')
                    subeenheidfactor = self.EENHEID[eenheid_naam][1]
                    eenheidbreuk = eenheidbreuk * subeenheidfactor
        for noemeronderdeel in noemeronderdelen:
            result = re.search(self.RE_NAAM_EENHEID, noemeronderdeel)
            if result is None:
                raise ValueError('noemeronderdeel van eenheid heeft ongeldige opmaak: \'{}\''.format(noemeronderdeel))
            else:
                eenheid_naam = result.group(1)
                eenheid_aantal = int(result.group(2)) if result.group(2) else 1
                if not eenheid_naam in self.EENHEID:
                    raise ValueError('noemeronderdeel van eenheid is onbekend: \'{}\''.format(eenheid_naam))
                for _ in range(eenheid_aantal):
                    weging = self.EENHEID[eenheid_naam][2]
                    if isinstance(weging, float) or isinstance(weging, int):
                        waarde = waarde * weging
                    elif isinstance(weging, tuple) and len(weging) == 3 \
                            and callable(weging[0]) and callable(weging[1]) \
                            and (isinstance(weging[2], float) or isinstance(weging[2], int)):
                        weging_noemerfactor = weging[2]
                        waarde = waarde * weging_noemerfactor
                    else:
                        raise ValueError('weging basiseenheid heeft verkeerde syntax')
                    subeenheidfactor = self.EENHEID[eenheid_naam][1]
                    eenheidbreuk = eenheidbreuk / subeenheidfactor
        if eenheidbreuk != oude_eenheidbreuk:
            raise ValueError('type eenheid \'{}\' komt niet overeen met type eenheid van waarde \'{}\''.format(eenheid, self.eenheidnaam))
        return waarde

    def _export_waarde(self, eenheid=None):
        """Exporteert interne waarde (getal) gegeven een eenheid."""
        if eenheid is None or eenheid == '' or eenheid == '-':
            return self.waarde
        else:
            return self._bereken_inverse_waarde(eenheid, self.waarde, self.eenheidbreuk)

    def __call__(self, eenheid=None):
        """Zet waarde om naar getal."""
        return self._export_waarde(eenheid)

    def __add__(self, andere_waarde):
        """Telt twee waarden bij elkaar op.

        >> Waarde(120, 'mm') + Waarde(30, 'cm')
        Waarde(0.42, 'm')
        """
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if not self.is_getal or not andere_waarde.is_getal:
            raise TypeError('beide waardes moeten getallen zijn')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        waarde = self.waarde + andere_waarde.waarde
        return Waarde(waarde, self.eenheidbreuk, config = self.config)


    def __sub__(self, andere_waarde):
        """Trekt waarde van andere waarde af.

        >> Waarde(520, 'mm') - Waarde(30, 'cm')
        Waarde(0.22, 'm')
        """
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if not self.is_getal or not andere_waarde.is_getal:
            raise TypeError('beide waardes moeten getallen zijn')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        waarde = self.waarde - andere_waarde.waarde
        return Waarde(waarde, self.eenheidbreuk, config = self.config)

    def __mul__(self, andere_waarde):
        """Vermenigvuldigt waarde met andere waarde of getal.

        >> Waarde(3, 'm') * Waarde(4, 's')
        Waarde(12.0, 'm*s')

        >> Waarde(3, 'm') * 6
        Waarde(18.0, 'm')
        """
        if (isinstance(andere_waarde, int) or isinstance(andere_waarde, float)):
            waarde = self.waarde * andere_waarde
            eenheidbreuk = self.eenheidbreuk
            return Waarde(waarde, eenheidbreuk, config = None)
        elif not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if not self.is_getal or not andere_waarde.is_getal:
            raise TypeError('beide waardes moeten getallen zijn')
        waarde = self.waarde * andere_waarde.waarde
        eenheidbreuk = self.eenheidbreuk * andere_waarde.eenheidbreuk
        return Waarde(waarde, eenheidbreuk, config = None)

    def __truediv__(self, andere_waarde):
        """Deelt waarde door andere waarde of getal.

        >> Waarde(20, 'ha') / Waarde(5, 'km')
        Waarde(40.0, 'm')

        >> Waarde(3, 'm') / 4
        Waarde(0.75, 'm')
        """
        if (isinstance(andere_waarde, int) or isinstance(andere_waarde, float)):
            waarde = self.waarde / andere_waarde
            eenheidbreuk = self.eenheidbreuk
            return Waarde(waarde, eenheidbreuk, config = None)
        elif not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if not self.is_getal or not andere_waarde.is_getal:
            raise TypeError('beide waardes moeten getallen zijn')
        if andere_waarde.waarde == 0:
            raise ZeroDivisionError('delen door 0 is niet mogelijk')
        waarde = self.waarde / andere_waarde.waarde
        eenheidbreuk = self.eenheidbreuk / andere_waarde.eenheidbreuk
        return Waarde(waarde, eenheidbreuk, config = None)

    def __pow__(self, macht):
        """Doet waarde tot de macht een andere waarde.

        >> Waarde(2, 'm') ** 3
        Waarde(8.0, 'm3')
        """
        if not isinstance(macht, int):
            raise TypeError('term is geen geheel getal')
        if not self.is_getal:
            raise TypeError('waarde moeten getal zijn')
        waarde = self.waarde ** macht
        eenheidbreuk = self.eenheidbreuk ** macht
        return Waarde(waarde, eenheidbreuk, config = None)

    def __rmul__(self, scalar):
        """Vermenigvuldigt getal met waarde.

        >> 2 * Waarde(4, 's')
        Waarde(8.0, 's')
        """
        if not (isinstance(scalar, int) or isinstance(scalar, float)):
            raise TypeError('term is geen getal')
        if not self.is_getal:
            raise TypeError('waarde moeten getal zijn')
        waarde = scalar * self.waarde
        eenheidbreuk = self.eenheidbreuk
        return Waarde(waarde, eenheidbreuk, config = self.config)

    def __rtruediv__(self, scalar):
        """Deelt getal met waarde.

        >> 2 / Waarde(4, 's')
        Waarde(0.5, '1/s')
        """
        if not (isinstance(scalar, int) or isinstance(scalar, float)):
            raise TypeError('term is geen getal')
        if not self.is_getal:
            raise TypeError('waarde moeten getal zijn')
        waarde = scalar / self.waarde
        eenheidbreuk = 1 / self.eenheidbreuk
        return Waarde(waarde, eenheidbreuk, config = self.config)

    def __eq__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: =="""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde == andere_waarde.waarde

    def __ne__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: !="""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde != andere_waarde.waarde

    def __lt__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: <"""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde < andere_waarde.waarde

    def __gt__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: >"""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde > andere_waarde.waarde

    def __le__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: <="""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde <= andere_waarde.waarde

    def __ge__(self, andere_waarde):
        """Vergelijkt waarde met andere waarde: >="""
        if not isinstance(andere_waarde, Waarde):
            raise TypeError('term is niet van type Waarde')
        if self.eenheidbreuk != andere_waarde.eenheidbreuk:
            raise TypeError('eenheden zijn niet zelfde type: {}, {}'.format(
                self.eenheidnaam, andere_waarde.eenheidnaam))
        return self.waarde >= andere_waarde.waarde

    def __repr__(self):
        if self.is_getal:
            return 'Waarde({}, \'{}\')'.format(self.waarde, self.eenheidnaam)
        else:
            return 'Waarde(\'{}\')'.format(self.waarde)

    def __str__(self):
        if 'standaard_eenheid' in self.config \
                and self.config['standaard_eenheid'] is not None \
                and self.config['standaard_eenheid'] != '' \
                and self.config['standaard_eenheid'] != '-':
            # wel een standaard eenheid
            if 'aantal_decimalen' in self.config \
                    and self.config['aantal_decimalen'] is not None:
                format_str = '{:.' + str(self.config['aantal_decimalen']) + 'f} {}'
                return format_str.format(
                    self._export_waarde(self.config['standaard_eenheid']),
                    self.config['standaard_eenheid'])
            else:
                format_str = '{:.' + str(self.STANDAARD_AANTAL_DECIMALEN) + 'f} {}'
                return format_str.format(
                    self._export_waarde(self.config['standaard_eenheid']),
                    self.config['standaard_eenheid'])
        elif self.is_getal and self.eenheidbreuk != Fraction(1):
            # geen standaard eenheid maar wel een dimensie
            if 'aantal_decimalen' in self.config \
                    and self.config['aantal_decimalen'] is not None:
                format_str = '{:.' + str(self.config['aantal_decimalen']) + 'f} {}'
                ehnaam = self.eenheidnaam
                return format_str.format(self._export_waarde(ehnaam), ehnaam)
            else:
                ehnaam = self.eenheidnaam
                return '{} {}'.format(self._export_waarde(ehnaam), ehnaam)
        else:
            # geen eenheid
            if self.is_getal:
                if 'aantal_decimalen' in self.config \
                        and self.config['aantal_decimalen'] is not None:
                    format_str = '{:.' + str(self.config['aantal_decimalen']) + 'f}'
                    return format_str.format(self.waarde)
                else:
                    return '{}'.format(self.waarde)
            else:
                return '{}'.format(self.waarde)

    #==========================================================================

    def _verander_aantal_decimalen(self, decimalen:int):
        """Helper functie voor eigenschappen qua standaard eenheid."""
        if not isinstance(decimalen, int):
            raise ValueError('aantal decimalen is geen geheel getal')
        self.config['aantal_decimalen'] = decimalen
        return self


    def _verander_eenheid(self, eenheid:str):
        """Helper functie voor eigenschappen qua afronding."""
        if not self.is_getal:
            raise ValueError('huide waarde is geen getal: {}'.format(self.waarde))
        if self.eenheidbreuk == Fraction(1):
            # waarde was dimensieloos; dan mogelijk om eenheid te veranderen
            self.__init__(self.waarde, eenheid)
        else:
            # waarde had een bepaalde eenheid; moet zelfde soort blijven
            tmp = Waarde(1.0, eenheid)
            if tmp.eenheidbreuk != self.eenheidbreuk:
                raise ValueError('huidig type eenheid ({}) komt niet overeen met nieuwe eenheid ({})'.format(self.eenheidbreuk, tmp.eenheidbreuk))
            self.__init__(self._export_waarde(eenheid), eenheid)
        return self

    def __getitem__(self, param:Union[int, str]):
        """Aanpassen van standaard eenheid of afronding."""
        if isinstance(param, int):
            return self._verander_aantal_decimalen(param)
        elif isinstance(param, str):
            return self._verander_eenheid(param)
        else:
            return self

    # AANTAL DECIMALEN

    @property
    def _0(self):
        return self._verander_aantal_decimalen(0)

    @property
    def _1(self):
        return self._verander_aantal_decimalen(1)

    @property
    def _2(self):
        return self._verander_aantal_decimalen(2)

    @property
    def _3(self):
        return self._verander_aantal_decimalen(3)

    @property
    def _4(self):
        return self._verander_aantal_decimalen(4)

    @property
    def _5(self):
        return self._verander_aantal_decimalen(5)

    @property
    def _6(self):
        return self._verander_aantal_decimalen(6)

    @property
    def _7(self):
        return self._verander_aantal_decimalen(7)

    @property
    def _8(self):
        return self._verander_aantal_decimalen(8)

    @property
    def _9(self):
        return self._verander_aantal_decimalen(9)

    # MASSA

    @property
    def ag(self):
        return self._verander_eenheid('ag')

    @property
    def fg(self):
        return self._verander_eenheid('fg')

    @property
    def pg(self):
        return self._verander_eenheid('pg')

    @property
    def ng(self):
        return self._verander_eenheid('ng')

    @property
    def mug(self):
        return self._verander_eenheid('mug')

    @property
    def mg(self):
        return self._verander_eenheid('mg')

    @property
    def cg(self):
        return self._verander_eenheid('cg')

    @property
    def dg(self):
        return self._verander_eenheid('dg')

    @property
    def g(self):
        return self._verander_eenheid('g')

    @property
    def hg(self):
        return self._verander_eenheid('hg')

    @property
    def kg(self):
        return self._verander_eenheid('kg')

    @property
    def Mg(self):
        return self._verander_eenheid('Mg')

    @property
    def Gg(self):
        return self._verander_eenheid('Gg')

    @property
    def Tg(self):
        return self._verander_eenheid('Tg')

    @property
    def Pg(self):
        return self._verander_eenheid('Pg')

    @property
    def Eg(self):
        return self._verander_eenheid('Eg')

    @property
    def ton(self):
        return self._verander_eenheid('ton')

    @property
    def kton(self):
        return self._verander_eenheid('kton')

    @property
    def Mton(self):
        return self._verander_eenheid('Mton')

    @property
    def ounce(self):
        return self._verander_eenheid('ounce')

    @property
    def pound(self):
        return self._verander_eenheid('pound')

    @property
    def kip(self):
        return self._verander_eenheid('kip')

    @property
    def stone(self):
        return self._verander_eenheid('stone')

    @property
    def grain(self):
        return self._verander_eenheid('grain')

    # LENGTE

    @property
    def am(self):
        return self._verander_eenheid('am')

    @property
    def fm(self):
        return self._verander_eenheid('fm')

    @property
    def pm(self):
        return self._verander_eenheid('pm')

    @property
    def nm(self):
        return self._verander_eenheid('nm')

    @property
    def mum(self):
        return self._verander_eenheid('mum')

    @property
    def mm(self):
        return self._verander_eenheid('mm')

    @property
    def cm(self):
        return self._verander_eenheid('cm')

    @property
    def dm(self):
        return self._verander_eenheid('dm')

    @property
    def m(self):
        return self._verander_eenheid('m')

    @property
    def dam(self):
        return self._verander_eenheid('dam')

    @property
    def hm(self):
        return self._verander_eenheid('hm')

    @property
    def km(self):
        return self._verander_eenheid('km')

    @property
    def Mm(self):
        return self._verander_eenheid('Mm')

    @property
    def Gm(self):
        return self._verander_eenheid('Gm')

    @property
    def Tm(self):
        return self._verander_eenheid('Tm')

    @property
    def Pm(self):
        return self._verander_eenheid('Pm')

    @property
    def Em(self):
        return self._verander_eenheid('Em')

    @property
    def inch(self):
        return self._verander_eenheid('in') # uitzondering

    @property
    def ft(self):
        return self._verander_eenheid('ft')

    @property
    def yard(self):
        return self._verander_eenheid('yard')

    @property
    def zeemijl(self):
        return self._verander_eenheid('zeemijl')

    @property
    def mijl(self):
        return self._verander_eenheid('mijl')

    # TIJD

    @property
    def attos(self):
        return self._verander_eenheid('as') # uitzondering

    @property
    def fs(self):
        return self._verander_eenheid('fs')

    @property
    def ps(self):
        return self._verander_eenheid('ps')

    @property
    def ns(self):
        return self._verander_eenheid('ns')

    @property
    def mus(self):
        return self._verander_eenheid('mus')

    @property
    def ms(self):
        return self._verander_eenheid('ms')

    @property
    def cs(self):
        return self._verander_eenheid('cs')

    @property
    def ds(self):
        return self._verander_eenheid('ds')

    @property
    def s(self):
        return self._verander_eenheid('s')

    @property
    def das(self):
        return self._verander_eenheid('das')

    @property
    def hs(self):
        return self._verander_eenheid('hs')

    @property
    def ks(self):
        return self._verander_eenheid('ks')

    @property
    def Ms(self):
        return self._verander_eenheid('Ms')

    @property
    def Gs(self):
        return self._verander_eenheid('Gs')

    @property
    def Ts(self):
        return self._verander_eenheid('Ts')

    @property
    def Ps(self):
        return self._verander_eenheid('Ps')

    @property
    def Es(self):
        return self._verander_eenheid('Es')

    @property
    def minuut(self):
        return self._verander_eenheid('min')  # uitzondering

    @property
    def h(self):
        return self._verander_eenheid('h')

    @property
    def d(self):
        return self._verander_eenheid('d')

    # TEMPERATUUR

    @property
    def C(self):
        return self._verander_eenheid('C')

    @property
    def K(self):
        return self._verander_eenheid('K')

    @property
    def F(self):
        return self._verander_eenheid('F')

    # HOEK

    @property
    def rad(self):
        return self._verander_eenheid('rad')

    @property
    def deg(self):
        return self._verander_eenheid('deg')

    @property
    def gon(self):
        return self._verander_eenheid('gon')

    # KRACHT

    @property
    def N(self):
        return self._verander_eenheid('N')

    @property
    def kN(self):
        return self._verander_eenheid('kN')

    @property
    def MN(self):
        return self._verander_eenheid('MN')

    @property
    def GN(self):
        return self._verander_eenheid('GN')

    @property
    def TN(self):
        return self._verander_eenheid('TN')

    # SPANNING

    @property
    def N_mm2(self):
        return self._verander_eenheid('N/mm2')

    @property
    def kN_mm2(self):
        return self._verander_eenheid('kN_mm2')

    @property
    def MN_mm2(self):
        return self._verander_eenheid('MN/mm2')

    @property
    def N_m2 (self):
        return self._verander_eenheid('N/m2')

    @property
    def kN_m2(self):
        return self._verander_eenheid('kN/m2')

    @property
    def MN_m2(self):
        return self._verander_eenheid('MN/m2')

    @property
    def Pa(self):
        return self._verander_eenheid('Pa')

    @property
    def kPa(self):
        return self._verander_eenheid('kPa')

    @property
    def MPa(self):
        return self._verander_eenheid('MPa')

    @property
    def GPa(self):
        return self._verander_eenheid('GPa')

    @property
    def TPa(self):
        return self._verander_eenheid('TPa')

    # MOMENT

    @property
    def Nm(self):
        return self._verander_eenheid('Nm')

    @property
    def kNm(self):
        return self._verander_eenheid('kNm')

    @property
    def MNm(self):
        return self._verander_eenheid('MNm')

    @property
    def Nmm(self):
        return self._verander_eenheid('Nmm')

    @property
    def kNmm(self):
        return self._verander_eenheid('kNmm')

    @property
    def MNmm(self):
        return self._verander_eenheid('MNmm')

    # OPPERVLAKTE

    @property
    def km2(self):
        return self._verander_eenheid('km2')

    @property
    def hm2(self):
        return self._verander_eenheid('hm2')

    @property
    def m2(self):
        return self._verander_eenheid('m2')

    @property
    def dm2(self):
        return self._verander_eenheid('dm2')

    @property
    def cm2(self):
        return self._verander_eenheid('cm2')

    @property
    def mm2(self):
        return self._verander_eenheid('mm2')

    @property
    def ca(self):
        return self._verander_eenheid('ca')

    @property
    def a(self):
        return self._verander_eenheid('a')

    @property
    def ha(self):
        return self._verander_eenheid('ha')

    # INHOUD

    @property
    def km3(self):
        return self._verander_eenheid('km3')

    @property
    def hm3(self):
        return self._verander_eenheid('hm3')

    @property
    def m3(self):
        return self._verander_eenheid('m3')

    @property
    def dm3(self):
        return self._verander_eenheid('dm3')

    @property
    def cm3(self):
        return self._verander_eenheid('cm3')

    @property
    def mm3(self):
        return self._verander_eenheid('mm3')

    @property
    def ml(self):
        return self._verander_eenheid('ml')

    @property
    def cl(self):
        return self._verander_eenheid('cl')

    @property
    def dl(self):
        return self._verander_eenheid('dl')

    @property
    def l(self):
        return self._verander_eenheid('l')

    @property
    def dal(self):
        return self._verander_eenheid('dal')

    @property
    def hl(self):
        return self._verander_eenheid('hl')

    @property
    def kl(self):
        return self._verander_eenheid('kl')

    @property
    def gallon(self):
        return self._verander_eenheid('gallon')

    @property
    def pint(self):
        return self._verander_eenheid('pint')

    @property
    def floz(self):
        return self._verander_eenheid('floz')

    @property
    def tbs(self):
        return self._verander_eenheid('tbs')

    @property
    def tsp(self):
        return self._verander_eenheid('tsp')

    @property
    def bbl(self):
        return self._verander_eenheid('bbl')

    @property
    def cup(self):
        return self._verander_eenheid('cup')

    # SNELHEID

    @property
    def km_j(self):
        return self._verander_eenheid('km/j')

    @property
    def km_d(self):
        return self._verander_eenheid('km/d')

    @property
    def km_h(self):
        return self._verander_eenheid('km/h')

    @property
    def km_min(self):
        return self._verander_eenheid('km/min')

    @property
    def km_s(self):
        return self._verander_eenheid('km/s')

    @property
    def m_j(self):
        return self._verander_eenheid('m/j')

    @property
    def m_d(self):
        return self._verander_eenheid('m/d')

    @property
    def m_h(self):
        return self._verander_eenheid('m/h')

    @property
    def m_min(self):
        return self._verander_eenheid('m/min')

    @property
    def m_s(self):
        return self._verander_eenheid('m/s')

    @property
    def dm_j(self):
        return self._verander_eenheid('dm/j')

    @property
    def dm_d(self):
        return self._verander_eenheid('dm/d')

    @property
    def dm_h(self):
        return self._verander_eenheid('dm/h')

    @property
    def dm_min(self):
        return self._verander_eenheid('dm/min')

    @property
    def dm_s(self):
        return self._verander_eenheid('dm/s')

    @property
    def cm_j(self):
        return self._verander_eenheid('cm/j')

    @property
    def cm_d(self):
        return self._verander_eenheid('cm/d')

    @property
    def cm_h(self):
        return self._verander_eenheid('cm/h')

    @property
    def cm_min(self):
        return self._verander_eenheid('cm/min')

    @property
    def cm_s(self):
        return self._verander_eenheid('cm/s')

    @property
    def mm_j(self):
        return self._verander_eenheid('mm/j')

    @property
    def mm_d(self):
        return self._verander_eenheid('mm/d')

    @property
    def mm_h(self):
        return self._verander_eenheid('mm/h')

    @property
    def mm_min(self):
        return self._verander_eenheid('mm/min')

    @property
    def mm_s(self):
        return self._verander_eenheid('mm/s')



    # TRAAGHEIDSMOMENT

    @property
    def km4(self):
        return self._verander_eenheid('km4')

    @property
    def m4(self):
        return self._verander_eenheid('m4')

    @property
    def dm4(self):
        return self._verander_eenheid('dm4')

    @property
    def cm4(self):
        return self._verander_eenheid('cm4')

    @property
    def mm4(self):
        return self._verander_eenheid('mm4')

    # DEBIET

    @property
    def km3_j(self):
        return self._verander_eenheid('km3/j')

    @property
    def km3_d(self):
        return self._verander_eenheid('km3/d')

    @property
    def km3_h(self):
        return self._verander_eenheid('km3/h')

    @property
    def km3_min(self):
        return self._verander_eenheid('km3/min')

    @property
    def km3_s(self):
        return self._verander_eenheid('km3/s')

    @property
    def m3_j(self):
        return self._verander_eenheid('m3/j')

    @property
    def m3_d(self):
        return self._verander_eenheid('m3/d')

    @property
    def m3_h(self):
        return self._verander_eenheid('m3/h')

    @property
    def m3_min(self):
        return self._verander_eenheid('m3/min')

    @property
    def m3_s(self):
        return self._verander_eenheid('m3/s')

    @property
    def dm3_j(self):
        return self._verander_eenheid('dm3/j')

    @property
    def dm3_d(self):
        return self._verander_eenheid('dm3/d')

    @property
    def dm3_h(self):
        return self._verander_eenheid('dm3/h')

    @property
    def dm3_min(self):
        return self._verander_eenheid('dm3/min')

    @property
    def dm3_s(self):
        return self._verander_eenheid('dm3/s')

    @property
    def cm3_j(self):
        return self._verander_eenheid('cm3/j')

    @property
    def cm3_d(self):
        return self._verander_eenheid('cm3/d')

    @property
    def cm3_h(self):
        return self._verander_eenheid('cm3/h')

    @property
    def cm3_min(self):
        return self._verander_eenheid('cm3/min')

    @property
    def cm3_s(self):
        return self._verander_eenheid('cm3/s')

    @property
    def mm3_j(self):
        return self._verander_eenheid('mm3/j')

    @property
    def mm3_d(self):
        return self._verander_eenheid('mm3/d')

    @property
    def mm3_h(self):
        return self._verander_eenheid('mm3/h')

    @property
    def mm3_min(self):
        return self._verander_eenheid('mm3/min')

    @property
    def mm3_s(self):
        return self._verander_eenheid('mm3/s')

    @property
    def l_j(self):
        return self._verander_eenheid('l/j')

    @property
    def l_d(self):
        return self._verander_eenheid('l/d')

    @property
    def l_h(self):
        return self._verander_eenheid('l/h')

    @property
    def l_min(self):
        return self._verander_eenheid('l/min')

    @property
    def l_s(self):
        return self._verander_eenheid('l/s')

    @property
    def dl_j(self):
        return self._verander_eenheid('dl/j')

    @property
    def dl_d(self):
        return self._verander_eenheid('dl/d')

    @property
    def dl_h(self):
        return self._verander_eenheid('dl/h')

    @property
    def dl_min(self):
        return self._verander_eenheid('dl/min')

    @property
    def dl_s(self):
        return self._verander_eenheid('dl/s')

    @property
    def cl_j(self):
        return self._verander_eenheid('cl/j')

    @property
    def cl_d(self):
        return self._verander_eenheid('cl/d')

    @property
    def cl_h(self):
        return self._verander_eenheid('cl/h')

    @property
    def cl_min(self):
        return self._verander_eenheid('cl/min')

    @property
    def cl_s(self):
        return self._verander_eenheid('cl/s')

    @property
    def ml_j(self):
        return self._verander_eenheid('ml/j')

    @property
    def ml_d(self):
        return self._verander_eenheid('ml/d')

    @property
    def ml_h(self):
        return self._verander_eenheid('ml/h')

    @property
    def ml_min(self):
        return self._verander_eenheid('ml/min')

    @property
    def ml_s(self):
        return self._verander_eenheid('ml/s')
