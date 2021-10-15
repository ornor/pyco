import pyco.toepassing as pycot
import pyco.model as pycom
import pyco.functies as pycof
import pyco.data as pycod
import pyco.interface as pycoi

import inspect

class Document(pycom.BasisObject):
    """
    Verzorgt in- en uitvoer van document.

    doc = pyco.interface.Document()
    x = doc.model.Waarde


    doc('Dit is wat tekst voor op document')

    @doc
    class berekening:

        a = x(120).cm   >>\
        "eerste parameter"

        b = x(4).m   >>\
        "volgende parameter"

    doc.print_rapport()
    """

    toepassing = pycot
    model = pycom
    data = pycod
    functies = pycof

    def __init__(self):
        super().__init__()

        self._klasses = []

    def _registreer(self, obj):
        if isinstance(obj, str):
            obj = pycom.Waarde(obj)
        if isinstance(obj, pycom.Waarde):
            class tmp:
                tmp = obj
            obj = tmp
        elif isinstance(obj, pycom.Figuur):
            class tmp:
                tmp = obj
            obj = tmp
        if inspect.isclass(obj):
            self._klasses.append((obj.__name__, obj))
        return obj

    def __call__(self, obj):
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
    def _componenten(self):
        comp_lijst = []
        for klasse_naam, obj_naam, obj in self._iter_klasse_objecten(pycom.BasisComponent):
            obj_nr = obj._object_nummer if hasattr(obj, '_object_nummer') else 0
            comp_lijst.append((obj_nr, klasse_naam, obj_naam, obj))
        comp_lijst = sorted(comp_lijst)
        return comp_lijst

    def toevoegen(self, obj):
        if isinstance(obj, str):
            obj = pycom.Waarde(obj)
        if isinstance(obj, pycom.Waarde):
            class tmp:
                tmp = obj

            self._registreer(tmp)


    def print_console(self, breedte_pagina:int = 80):
        lijn = breedte_pagina * '-'
        laatste_klasse_naam = None
        for _, klasse_naam, obj_naam, obj in self._componenten:
            if laatste_klasse_naam != klasse_naam and klasse_naam != 'tmp':
                print()
                print(lijn)
                print(klasse_naam.upper())
                print(lijn)
                laatste_klasse_naam = klasse_naam
            naam = obj_naam
            str_obj = str(obj)

            if isinstance(obj, pycom.Waarde):
                print()

                if str_obj[-2:] == ' -':
                    str_obj = str_obj[:-2]

                if naam != 'tmp':
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        print('{}\n{} = {}'.format(obj._documentatie, naam, str_obj))
                    else:
                        print('{} = {}'.format(naam, str_obj))
                else:
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        print('{}\n{}'.format(obj._documentatie, str_obj))
                    else:
                        print('{}'.format(str_obj))
            elif isinstance(obj, pycom.Figuur):
                obj.plot_console()
        print()

    def print_html(self):

        html = pycoi.Html()

        html.title = 'PYCO document'
        html.body('<h1>' + html.title + '</h1>')

        laatste_klasse_naam = None
        for _, klasse_naam, obj_naam, obj in self._componenten:
            if laatste_klasse_naam != klasse_naam and klasse_naam != 'tmp':
                html.body('<h2>' + klasse_naam.upper() + '</h2>')
                laatste_klasse_naam = klasse_naam
            naam = obj_naam
            str_obj = str(obj)

            if isinstance(obj, pycom.Waarde):

                if str_obj[-2:] == ' -':
                    str_obj = str_obj[:-2]

                if naam != 'tmp':
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        html.body('<pre>{}\n{} = {}</pre>'.format(obj._documentatie, naam, str_obj))
                    else:
                        html.body('<pre>{} = {}</pre>'.format(naam, str_obj))
                else:
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        html.body('<pre>{}\n{}</pre>'.format(obj._documentatie, str_obj))
                    else:
                        html.body('<pre>{}</pre>'.format(str_obj))
            elif isinstance(obj, pycom.Figuur):
                html.body(obj.png_html_code())

        html.openen_in_browser()
