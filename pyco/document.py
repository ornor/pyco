import inspect

import IPython.display

import pyco.basis
import pyco.waarde
import pyco.figuur

class pc:
    BasisObject = pyco.basis.BasisObject
    Waarde = pyco.waarde.Waarde
    Figuur = pyco.figuur.Figuur
    

class Document(pc.BasisObject):
    """
    Framework voor gestructureerde uitvoer.
    
    doc = pc.Document

    """
    
    def __init__(self, titel=None):
        super().__init__()

        self._titel = 'Pyco document' if titel is None else titel

        self._klasses = []

    def _registreer(self, obj):
        if isinstance(obj, str):
            obj = pc.Waarde(obj)
        if isinstance(obj, pc.Waarde):
            class tmp:
                tmp = obj
            obj = tmp
        elif isinstance(obj, pc.Figuur):
            class tmp:
                tmp = pc.Waarde(obj.png_html)
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
        for klasse_naam, obj_naam, obj in self._iter_klasse_objecten(pc.BasisObject):
            obj_nr = obj._object_nummer if hasattr(obj, '_object_nummer') else 0
            comp_lijst.append((obj_nr, klasse_naam, obj_naam, obj))
        comp_lijst = sorted(comp_lijst)
        return comp_lijst
    
    def _print(self, html_str):
        IPython.display.display(IPython.display.HTML(html_str))
    
    @property
    def titel(self):
        return self._titel
    
    @titel.setter
    def titel(self, tekst):
        self._titel = tekst
    
    def weergeven(self, breedte_pagina:int = 80):
        html = '<h1>{}</h1>'.format(self.titel)
        
        def html_rij(omschrijving, naam, waarde):
            cel1 = 'width:65%;text-align:left;'
            cel2 = 'width:35%;text-align:left;'
            if naam is None:
                return '<tr><td style="{}">{}</td><td style="{}">{}</td></tr>'.format(cel1, omschrijving, cel2, waarde)
            else:
                return '<tr><td style="{}">{}</td><td style="{}">{} = {}</td></tr>'.format(cel1, omschrijving, cel2, naam, waarde)

        laatste_klasse_naam = None
        html += '<table style="display:none;"><tbody>'
        for _, klasse_naam, obj_naam, obj in self._componenten:
            if laatste_klasse_naam != klasse_naam and klasse_naam != 'tmp':
                html += '</tbody></table>'
                html += '<h2>{}</h2>'.format(klasse_naam.replace('_', ' '))
                html += '<table style="width:90%;"><tbody>'
                laatste_klasse_naam = klasse_naam
            naam = obj_naam
            str_obj = str(obj)

            if isinstance(obj, pc.Waarde):
                if str_obj[-2:] == ' -':
                    str_obj = str_obj[:-2]

                if naam != 'tmp':
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        html += html_rij(obj._documentatie, naam, str_obj)
                    else:
                        html += html_rij('&nbsp;', naam, str_obj)
                else:
                    if hasattr(obj, '_documentatie') and obj._documentatie:
                        html += html_rij(obj._documentatie, None, str_obj)
                    else:
                        html += html_rij(str_obj, None, '&nbsp;')
            elif isinstance(obj, pc.Figuur):
                html += obj.png_html
            else:
                pass # all other types of objects
        html += '</tbody></table>'
            
        self._print(html)
