import inspect

import IPython.display

import pyco.basis
import pyco.waarde
import pyco.figuur

class pc:
    BasisObject = pyco.basis.BasisObject
    Waarde = pyco.waarde.Waarde
    Figuur = pyco.figuur.Figuur
    
    
class html_lib: 
    CEL_ACHTERGROND_KLEUR = '#fff'
    CEL_ACHTERGROND_KLEUR_KOP1 = '#fff'
    CEL_ACHTERGROND_KLEUR_KOP2 = '#eee'
    
    LIJN_STIJL = '1px solid #888'
    LIJN_LINKS_STIJL = '2px solid #888' # met 1px is lijn niet zichtbaar
    LIJN_RECHTS_STIJL = '1px solid #888'
    
    CEL1_STIJL = f'text-align:left;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR};'
    CEL1_BREEDTE = 100
    
    CEL2_STIJL = f'text-align:right;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR};'
    CEL2_BREEDTE = 80
    
    CEL3_STIJL = f'text-align:left;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR};'
    CEL3_BREEDTE = 60
    
    CEL4_STIJL = f'text-align:right;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR};'
    CEL4_BREEDTE = 530
    
    CEL_FIGUUR_STIJL = f'text-align:center;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR};'

    KOP1_CEL_STIJL = f'text-align:left;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR_KOP1};'
    KOP1_TEKST_STIJL = 'font-weight:bold;font-size:1.9em;'
    
    KOP2_CEL_STIJL = f'text-align:left;vertical-align:top;background-color:{CEL_ACHTERGROND_KLEUR_KOP2};border-top:{LIJN_STIJL};border-bottom:{LIJN_STIJL};'
    KOP2_TEKST_STIJL = 'font-weight:normal;font-size:1.5em;'
    
    
    @staticmethod
    def spacer(breedte, hoogte):
        return f'<img href="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEAAAEALAAAAAABAAEAAAICTAEAOw==" width="{breedte}" height="{hoogte}" border="0" style="width:{breedte}px;height:{hoogte}px;border:0px;"/>'

    @staticmethod
    def lege_regel():
        return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}width:{html_lib.CEL1_BREEDTE}px;">
        {html_lib.spacer(html_lib.CEL1_BREEDTE, 1)}
    </td>
    <td style="{html_lib.CEL2_STIJL}width:{html_lib.CEL2_BREEDTE}px;">
        {html_lib.spacer(html_lib.CEL2_BREEDTE, 1)}
    </td>
    <td style="{html_lib.CEL3_STIJL}width:{html_lib.CEL3_BREEDTE}px;">
        {html_lib.spacer(html_lib.CEL3_BREEDTE, 1)}
    </td>
    <td style="{html_lib.CEL4_STIJL}width:{html_lib.CEL4_BREEDTE}px;">
        {html_lib.spacer(html_lib.CEL4_BREEDTE, 1)}
    </td>
</tr>"""
    
    @staticmethod
    def tabel_start():
        return '<table><tbody>' + html_lib.lege_regel()
    
    @staticmethod
    def tabel_einde():
        return '</tbody></table>'
    
    @staticmethod
    def lijn(boven=True):
        positie = 'top' if boven else 'bottom'
        return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}border-{positie}:{html_lib.LIJN_STIJL};">
        {html_lib.spacer(1, 1)}
    </td>
    <td style="{html_lib.CEL2_STIJL}border-{positie}:{html_lib.LIJN_STIJL};">
        {html_lib.spacer(1, 1)}
    </td>
    <td style="{html_lib.CEL3_STIJL}border-{positie}:{html_lib.LIJN_STIJL};">
        {html_lib.spacer(1, 1)}
    </td>
    <td style="{html_lib.CEL4_STIJL}border-{positie}:{html_lib.LIJN_STIJL};">
        {html_lib.spacer(1, 1)}
    </td>
</tr>"""
    
    @staticmethod
    def kop1(tekst):
        return f"""
<tr>
    <td colspan="4" style="{html_lib.KOP1_CEL_STIJL}">
        <span style="{html_lib.KOP1_TEKST_STIJL}">{tekst}</span>
    </td>
</tr>"""
    
    @staticmethod
    def kop2(tekst):
        return f"""
<tr>
    <td colspan="4" style="{html_lib.KOP2_CEL_STIJL}">
        <span style="{html_lib.KOP2_TEKST_STIJL}">{tekst}</span>
    </td>
</tr>"""
    
    @staticmethod
    def tekst(naam, tekst, docu):
        if naam == '' and docu == '':
            return f"""
<tr>
    <td colspan="4" style="{html_lib.CEL1_STIJL}">
        <span style="">{tekst}</span>
    </td>
</tr>"""
        elif naam == '':
            return f"""
<tr>
    <td colspan="3" style="{html_lib.CEL1_STIJL}">
        <span style="">{tekst}</span>
    </td>
    <td style="{html_lib.CEL4_STIJL}">
        <span style="">{docu}</span>
    </td>
</tr>"""
        elif docu == '':
            return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}">
        <span style="">${naam}$</span>
    </td>
    <td style="{html_lib.CEL2_STIJL}">
        <span style="">{html_lib.spacer(1, 1)}</span>
    </td>
    <td colspan="2" style="{html_lib.CEL3_STIJL}">
        <span style="">{tekst}</span>
    </td>
</tr>"""
        else:
            return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}">
        <span style="">${naam}$</span>
    </td>
    <td style="{html_lib.CEL2_STIJL}">
        <span style="">{html_lib.spacer(1, 1)}</span>
    </td>
    <td style="{html_lib.CEL3_STIJL}">
        <span style="">{tekst}</span>
    </td>
    <td style="{html_lib.CEL4_STIJL}">
        <span style="">{docu}</span>
    </td>
</tr>"""
    
    @staticmethod
    def figuur(naam, obj):
        naam = '$' + naam + '$' if naam != '' else '&nbsp;'
        
        return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}">{naam}</td>
    <td colspan="3" style="{html_lib.CEL_FIGUUR_STIJL};">{obj.png_html}</td>
</tr>"""
        
    @staticmethod
    def waarde(naam, obj, docu):
        naam = '$' + naam + '$' if naam != '' else '&nbsp;'
        
        _1 = naam
        waarde_str = str(obj)
        _2 = waarde_str
        _3 = ''
        if ' ' in waarde_str:
            _2 = waarde_str.split(' ', 2)[0]
            _3 = waarde_str.split(' ', 2)[1]
        _4 = docu
        
        return f"""
<tr>
    <td style="{html_lib.CEL1_STIJL}">
        <span>{_1}</span>
    </td>
    <td style="{html_lib.CEL2_STIJL}">
        <span>{_2}</span>
    </td>
    <td style="{html_lib.CEL3_STIJL}">
        <span>{_3}</span>
    </td>
    <td style="{html_lib.CEL4_STIJL}">
        <span>{_4}</span>
    </td>
</tr>"""


class Document(pc.BasisObject):
    """
    Framework voor gestructureerde uitvoer.
    
    doc = pc.Document

    """
    
    TYPE_TEKST = 0
    TYPE_KLASSE_START = 1
    TYPE_KLASSE_EINDE = 2
    TYPE_FUNCTIE = 3
    TYPE_WAARDE = 4
    TYPE_FIGUUR = 5
    TYPE_PYCO_OVERIG = 6
    
    SPECIALE_LETTERS = sorted('alpha nu beta Xi xi Gamma gamma Delta delta Pi pi varpi epsilon varepsilon rho varrho zeta Sigma sigma varsigma eta tau Theta theta vartheta Upsilon upsilon iota Phi phi varphi kappa varkappa chi Lambda lambda Psi psi mu Omega omega partial infty'.split())
    
    def __init__(self, titel:str=None):
        super().__init__()

        self._titel = None
        if titel is not None:
            self._titel = titel.capitalize()
            
        self._onderdelen = []  # (type, naam, object, documentatie)
        
    #---------------------------------------------------------------------------
        
    def _print(self, md_str):
        IPython.display.display(IPython.display.HTML(md_str))
        
    def __call__(self, obj=None):
        if obj is None:
            self._print(self.html)
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
        return None
        
    def _registreer_klasse(self, obj, naam):
        naam =  (obj.__name__[0].capitalize() + obj.__name__.replace('_', ' ')[1:]) if naam is None else naam
        documentatie = ''
        
        self._onderdelen.append((self.TYPE_KLASSE_START, naam, obj, documentatie))
        
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
            
        self._onderdelen.append((self.TYPE_KLASSE_EINDE, naam, obj, documentatie))
        
        return obj
    
    def _registreer_functie(self, obj, naam):
        naam = (obj.__name__[0].capitalize() + obj.__name__.replace('_', ' ')[1:]) if naam is None else naam
        documentatie = ''
        self._onderdelen.append((self.TYPE_FUNCTIE, naam, obj, documentatie))
        return obj
    
    def _registreer_waarde(self, obj, naam):
        naam = '' if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_WAARDE, naam, obj, documentatie))
        return None
    
    def _registreer_figuur(self, obj, naam):
        naam = obj.titel if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_FIGUUR, naam, obj, documentatie))
        return None
    
    def _registreer_pyco_overig(self, obj, naam):
        naam = '' if naam is None else naam
        documentatie = obj._documentatie if hasattr(obj, '_documentatie') else ''
        self._onderdelen.append((self.TYPE_PYCO_OVERIG, naam, obj, documentatie))
        return None
    
    #---------------------------------------------------------------------------
        
    def _vervang_naam(self, naam):
        klasse_naam = ''
        if '.' in naam:
            klasse_naam, naam = tuple(naam.split('.', 2))
        
        delen = naam.split('_')
        for ideel, deel in enumerate(delen):
            if deel in self.SPECIALE_LETTERS:
                delen[ideel] = '\\' + deel
        if len(delen) == 1:
            return klasse_naam, delen[0]
        elif len(delen) == 2:
            return klasse_naam, delen[0] + '_{' + delen[1] + '}'
        else:
            return klasse_naam, delen[0] + '_{' + ','.join(delen[1:]) + '}'
        
    @property
    def html(self):
        html = ''
        
        html += html_lib.tabel_start()
        
        if self._titel is not None:
            html += html_lib.kop1(self._titel)
        
        for typ, naam, obj, docu in self._onderdelen:
            if typ == self.TYPE_TEKST:
                html += html_lib.tekst(self._vervang_naam(naam)[1], obj, docu)
            elif typ == self.TYPE_KLASSE_START:
                html += html_lib.lege_regel()
                html += html_lib.kop2(naam)
            elif typ == self.TYPE_KLASSE_EINDE:
                html += html_lib.lijn(boven=True)
            elif typ == self.TYPE_FUNCTIE:
                pass
            elif typ == self.TYPE_WAARDE:
                html += html_lib.waarde(self._vervang_naam(naam)[1], obj, docu)
            elif typ == self.TYPE_FIGUUR:
                html += html_lib.figuur(self._vervang_naam(naam)[1], obj)
            elif typ == self.TYPE_PYCO_OVERIG:
                pass
        
        html += html_lib.tabel_einde()
        
        return html