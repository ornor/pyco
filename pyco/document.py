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
    
    TYPE_TEKST = 0
    TYPE_KLASSE = 1
    TYPE_FUNCTIE = 2
    TYPE_WAARDE = 3
    TYPE_FIGUUR = 4
    TYPE_PYCO_OVERIG = 5
    
    SPECIALE_LETTERS = sorted('alpha nu beta Xi xi Gamma gamma Delta delta Pi pi varpi epsilon varepsilon rho varrho zeta Sigma sigma varsigma eta tau Theta theta vartheta Upsilon upsilon iota Phi phi varphi kappa varkappa chi Lambda lambda Psi psi mu Omega omega partial infty'.split())
    
    def __init__(self, titel:str=None):
        super().__init__()

        self._titel = None
        if titel is not None:
            self._titel = titel.capitalize()
            self._print_kop1(self._titel)
            
        self._onderdelen = []  # (type, naam, object, documentatie)
        
    #---------------------------------------------------------------------------
        
    def __call__(self, obj):
        return self._registreer(obj)
        
    def _registreer(self, obj, naam=None):
        if isinstance(obj, str):
            return self._registreer_tekst(obj, naam)
        elif inspect.isclass(obj):
            return self._registreer_klasse(obj, naam)
        elif inspect.isfunction(obj):
            return self._registreer_functie(obj, naam)
        elif isinstance(obj, pc.Waarde):
            return self._registreer_waarde(obj, naam)
        elif isinstance(obj, pc.Figuur):
            return self._registreer_figuur(obj, naam)
        elif isinstance(obj, pc.BasisObject):
            return self._registreer_pyco_overig(obj, naam)
            
    def _registreer_tekst(self, obj, naam):
        naam = '' if naam is None else naam
        documentatie = ''
        self._onderdelen.append((self.TYPE_TEKST, naam, obj, documentatie))
        self._print_tekst(obj)
        return None
        
    def _registreer_klasse(self, obj, naam):
        naam =  (obj.__name__[0].capitalize() + obj.__name__.replace('_', ' ')[1:]) if naam is None else naam
        documentatie = ''
        self._onderdelen.append((self.TYPE_KLASSE, naam, obj, documentatie))
        self._print_kop2(naam)
        
        klasse_naam = obj.__name__
        onderdelen_lijst = []
        for sub_obj_naam in dir(obj):
            sub_obj = getattr(obj, sub_obj_naam)
            if not isinstance(sub_obj, pc.BasisObject):
                continue
            obj_nr = sub_obj._object_nummer if hasattr(sub_obj, '_object_nummer') else 0
            onderdelen_lijst.append((obj_nr, klasse_naam, sub_obj_naam, sub_obj))
        
        for _, klasse_naam, ond_naam, ond_obj in sorted(onderdelen_lijst):
            self._registreer(ond_obj, '{}.{}'.format(klasse_naam, ond_naam))
        return obj
    
    def _registreer_functie(self, obj, naam):
        naam = (obj.__name__[0].capitalize() + obj.__name__.replace('_', ' ')[1:]) if naam is None else naam
        documentatie = ''
        self._onderdelen.append((self.TYPE_FUNCTIE, naam, obj, documentatie))
        self._print_kop2(naam)
        # TODO
        return obj
    
    def _registreer_waarde(self, obj, naam):
        naam = '' if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_WAARDE, naam, obj, documentatie))
        self._print_waarde(obj, naam, documentatie)
        return None
    
    def _registreer_figuur(self, obj, naam):
        naam = obj.titel if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_FIGUUR, naam, obj, documentatie))
        self._print_figuur(obj, naam, documentatie)
        return None
    
    def _registreer_pyco_overig(self, obj, naam):
        naam = '' if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_PYCO_OVERIG, naam, obj, documentatie))
        if hasattr(obj, 'plot'):
            obj.plot()
        else:
            self._print_waarde(pc.Waarde(repr(obj)), naam, documentatie)
        return None
    
    #---------------------------------------------------------------------------
    
    def _print_html(self, html_str):
        IPython.display.display(IPython.display.HTML(html_str))
    
    def _print_markdown(self, md_str):
        IPython.display.display(IPython.display.Markdown(md_str))
        
    def _print_kop1(self, tekst):
        self._print_markdown('# {}'.format(tekst))
        
    def _print_kop2(self, tekst):
        self._print_markdown('## {}'.format(tekst))
        
    def _print_tekst(self, tekst):
        self._print_markdown('{}'.format(tekst))
        
    def _vervang_naam(self, naam):
        delen = naam.split('_')
        for ideel, deel in enumerate(delen):
            if deel in self.SPECIALE_LETTERS:
                delen[ideel] = '\\' + deel
        if len(delen) == 1:
            return delen[0]
        elif len(delen) == 2:
            return delen[0] + '_' + delen[1]
        else:
            return delen[0] + '_{' + ','.join(delen[1:]) + '}'
        
    def _print_waarde(self, waarde_obj, naam, documentatie):
        klasse_naam = ''
        if '.' in naam:
            klasse_naam, naam = tuple(naam.split('.', 2))
        naam = self._vervang_naam(naam)
        
        _1 = documentatie
        _2 = naam
        
        if not waarde_obj._is_getal:
            _3 = str(waarde_obj)
            if _1 and _2:
                self._print_markdown('$' + _2 + ' = \\:$' + _3 + '$\\quad$ *' + _1 +'*')
            elif _1:
                self._print_markdown('' + _3 + '$\\quad$ *' + _1 +'*')
            elif _2:
                self._print_markdown('$' + _2 + ' = \\:$' + _3 + '')
            else:
                self._print_markdown(_3)
            return
        
        _3 = str(waarde_obj).split()[0]
        _4 = waarde_obj.eenheid if waarde_obj.eenheid is not None else ''
        
        if _1 and _2 and _4:
            self._print_markdown('$' + _2 + ' = ' + _3 + '\\: \\mathrm{' + _4 + '} \\quad$ *' + _1 + '*')
        elif _1 and _2:
            self._print_markdown('$' + _2 + ' = ' + _3 + '\\quad$ *' + _1 + '*')
        elif _1 and _4:
            self._print_markdown('$' + _3 + '\\: \\mathrm{' + _4 + '} \\quad$ *' + _1 + '*')
        elif _1:
            self._print_markdown('$' + _3 + '\\quad$ *' + _1 + '*')
        elif _2 and _4:
            self._print_markdown('$' + _2 + ' = ' + _3 + '\\: \\mathrm{' + _4 + '}$')
        elif _2:
            self._print_markdown('$' + _2 + ' = ' + _3 + '$')
        elif _4:
            self._print_markdown('$' + _3 + '\\: \\mathrm{' + _4 + '}$')
        else:
            self._print_markdown('$' + _3 + '$')
            
    def _print_figuur(self, figuur_obj, naam, documentatie):
        self._print_html('{}'.format(figuur_obj.png_html))
        
    
    
