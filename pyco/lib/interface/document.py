import pyco.toepassing as pycot
import pyco.model as pycom
import pyco.functies as pycof
import pyco.data as pycod

import inspect

class Document(pycom.BasisObject):

    toepassing = pycot
    model = pycom
    data = pycod
    functies = pycof

    def __init__(self):
        super().__init__()

        self._klasses = []

    def _registreer(self, obj):
        if inspect.isclass(obj):
            self._klasses.append((obj.__name__, obj))
        return obj

    def __call__(self, obj):
        """"
        Decorator functie registreert klasse.

        doc = pyco.interface.Document()
        x = doc.model.Waarde

        @doc
        class berekening:

            # eerste parameter
            a = x(120).cm

            # volgende parameter
            b = x(4).m

        doc.print_rapport()
        """
        return self._registreer(obj)

    def _iter_klasse_objecten(self, filter_obj_type=None):
        for klasse_naam, klasse in self._klasses:
            for obj_naam in dir(klasse):
                obj = getattr(klasse, obj_naam)
                if filter_obj_type is not None:
                    if isinstance(obj, filter_obj_type):
                        yield klasse_naam, obj_naam, obj
                else:
                    yield klasse_naam, obj_naam, obj

    @property
    def _waardes(self):
        waarde_lijst = []
        for klasse_naam, obj_naam, obj in self._iter_klasse_objecten(pycom.Waarde):
            obj_nr = obj._object_nummer if hasattr(obj, '_object_nummer') else 0
            waarde_lijst.append((obj_nr, klasse_naam, obj_naam, obj))
        waarde_lijst = sorted(waarde_lijst)
        return waarde_lijst

    def print_rapport(self, len_omschrijving:int = 16, len_waarde:int = 12,
                      breedte_pagina:int = 80):
        lijn = breedte_pagina * '-'
        laatste_klasse_naam = None
        for _, klasse_naam, obj_naam, obj in self._waardes:
            if laatste_klasse_naam != klasse_naam:
                print()
                print(lijn)
                print(klasse_naam)
                print(lijn)
                laatste_klasse_naam = klasse_naam
            naam = obj_naam
            waarde = str(obj)
            if waarde[-2:] == ' -':
                waarde = waarde[:-2]
            print()
            # format_str = '{}\n{:' + str(len_omschrijving) + '.' \
            #     + str(len_omschrijving) + 's} = {:' + str(len_waarde) + 's}'
            if hasattr(obj, '_documentatie') and obj._documentatie:
                print('{}\n{} = {}'.format(obj._documentatie, naam, waarde))
            else:
                print('{} = {}'.format(naam, waarde))
        print()
