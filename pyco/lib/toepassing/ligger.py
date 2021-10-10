from typing import Union, List, Dict

import pyco.model as pycom
import pyco.functies as pycof


class Ligger(pycom.BasisObject):
    """Met deze toepassing kan een ligger worden doorgerekend.

    import pyco.toepassing as pycot
    import pyco.model as pycom

    lg = pycot.Ligger()

    # eenmalig standaard eenheid definiëren
    lg.knoop_eenheid = 'm'
    # invoer van pyco.Waarde
    lg.knoop(naam='k1', x=pycom.Waarde(0, 'm'))
    # of met (eenmaal) ingevoerde knoop_eenheid, alleen invoer van waarde
    lg.knoop('k2', 9)
    # knoop objecten kunnen worden bewaard
    k3_obj = lg.knoop('k3', 14)
    nog_meer_knopen = {'k4': 20, 'k5': 23}
    # dit mag ook een map zijn (ingevuld bij naam of x)
    lg.knoop(nog_meer_knopen)
    # auto nummering van knopen (k6 etc.)
    lg.knoop('k', [25, 27, 29])

    # invoer via naam
    lg.staaf(naam='s1', knoop1=lg['k1'], knoop2=lg['k2'])
    # of rechtstreeks met Knoop object
    lg.staaf('s2', lg['k2'], k3_obj)
    # of alleen naam-tekst
    lg.staaf('s3', 'k3', 'k4')
    lg.staaf('s4', 'k4', 'k5')

    """

    def __init__(self):
        super().__init__()

        # standaard eenheid
        self._knoop_eenheid = 'm'
        # standaard prefix voor automatische knoopnummering
        self._knoop_prefix = 'k'

    @property
    def knoop_eenheid(self) -> str:
        """Ophalen van standaard knoopeenheid.

        Deze wordt gebruikt indien alleen een getal (zonder eenheid) is
        gegeven.
        """

        return self._knoop_eenheid

    @knoop_eenheid.setter
    def knoop_eenheid(self, eenheid: str):
        """Definiëren van standaard knoopeenheid.

        Deze wordt gebruikt indien alleen een getal (zonder eenheid) is
        gegeven.
        """

        # geef een foutmelding als eenheid incorrect is ingevoerd
        #   (door een tijdelijk Waarde object aan te maken)
        pycom.Waarde(1, eenheid)

        self._knoop_eenheid = eenheid

    def knoop(self,
              naam: Union[str, dict] = None,
              x: Union[pycom.Waarde, int, float, list, tuple, dict] = None) \
            -> Union[pycom.Knoop, List[pycom.Knoop]]:
        """Definieer één knoop of meerdere knopen."""

        # als 'x' is een lijst en 'naam' is opgegeven, dan dient
        #   'naam' als een prefix voor de auto knoopnummering van lijst
        if pycof.is_tekst_en_niet_leeg(naam) \
                and pycof.is_lijst_of_tupel_en_niet_leeg(x):
            gevonden_knoopnamen = []

            def vind_knoopnaam() -> str:
                gevonden = False
                knoopnummer = 1
                while not gevonden:
                    knoopnaam = '{}{}'.format(naam, knoopnummer)
                    if knoopnaam not in self.objecten \
                            and knoopnaam not in gevonden_knoopnamen:
                        gevonden = True
                    else:
                        knoopnummer += 1
                gevonden_knoopnamen.append(knoopnaam)
                return knoopnaam

            knopen_map = {}
            for knoopwaarde in x:
                knopen_map[vind_knoopnaam()] = knoopwaarde
            # vervang de waarde 'x' door een map
            x = knopen_map

        # als 'naam' een dictionary is, dan wordt deze ingelezen als invoer
        #   van meerdere knopen; 'x' wordt genegeerd
        if pycof.is_map_en_niet_leeg(naam):
            # vervang de waarde 'x' door een map
            x = naam

        # als 'x' een dictionary is, dan wordt deze ingelezen als invoer
        #   van meerdere knopen; 'naam' wordt genegeerd
        if pycof.is_map_en_niet_leeg(x):
            knopen_map = x
            knopen_objecten = {}
            for knoop_k, knoop_v in knopen_map.items():
                # voor iedere knoop in lijst, gebruik recursief deze methode
                knoop = self.knoop(knoop_k, knoop_v)
                knopen_objecten[knoop_k] = knoop
            return knopen_objecten

        if naam is None or x is None:
            raise ValueError('naam en x-waarde zijn verplicht')

        # als 'x' alleen een getal is, gebruik standaard knoopeenheid
        if pycof.is_getal(x):
            x = pycom.Waarde(x, self._knoop_eenheid)

        knoop = pycom.Knoop(x=x)
        self.__setitem__(naam, knoop)
        return knoop

    @property
    def knopen(self) -> Dict[str, pycom.Knoop]:
        """Ophalen map van knoopnamen met knoopobjecten."""
        return self.objecten_van_klasse(pycom.Knoop)

    def staaf(self, naam: str = None,
              knoop1: Union[pycom.Knoop, str] = None,
              knoop2: Union[pycom.Knoop, str] = None) \
            -> pycom.Staaf:
        """Definieer één staaf of meerdere staven."""
        if naam is None or knoop1 is None or knoop2 is None:
            raise ValueError('naam, knoop1 en knoop2 zijn verplicht')
        if isinstance(knoop1, str):
            knoop1 = self[knoop1]
        if isinstance(knoop2, str):
            knoop2 = self[knoop2]
        lijn = pycom.Lijn(knoop1, knoop2)
        staaf = pycom.Staaf(lijn=lijn)
        self.__setitem__(naam, staaf)
        return staaf

    @property
    def staven(self) -> Dict[str, pycom.Staaf]:
        """Ophalen map van staafnamen met staafobjecten."""
        return self.objecten_van_klasse(pycom.Staaf)

    def __repr__(self):
        return 'Ligger()'.format()
