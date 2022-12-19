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
        
    #---------------------------------------------------------------------------
    
    def _html_spacer(self, breedte, hoogte):
        return f'<img href="data:image/gif;base64,R0lGODlhAQABAIAAAP///////yH5BAEAAAEALAAAAAABAAEAAAICTAEAOw==" width="{breedte}" height="{hoogte}"/>'
        
    def _html_tabel_lege_regel(self):
        return f"""
<tr>
    <td style="text-align:left;vertical-align:top;background-color:#fff;width:100px;">
        {self._html_spacer(100, 1)}
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;width:80px;">
        {self._html_spacer(80, 1)}
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;width:60px;">
        {self._html_spacer(60, 1)}
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;width:530px;">
        {self._html_spacer(530, 1)}
    </td>
</tr>"""
    
    def _html_tabel_lijn(self, boven=True):
        positie = 'top' if boven else 'bottom'
        lijn_stijl = '1px solid #888'
        return f"""
<tr>
    <td style="text-align:left;vertical-align:top;background-color:#fff;border-{positie}:{lijn_stijl};">
        {self._html_spacer(1, 1)}
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;border-{positie}:{lijn_stijl};">
        {self._html_spacer(1, 1)}
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;border-{positie}:{lijn_stijl};">
        {self._html_spacer(1, 1)}
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;border-{positie}:{lijn_stijl};">
        {self._html_spacer(1, 1)}
    </td>
</tr>"""
    
    def _html_tabel_start(self):
        return '<table><tbody>' + self._html_tabel_lege_regel()
        
    def _html_tabel_einde(self):
        return '</tbody></table>'
    
    def _html_tabel_kop1(self, tekst):
        return f"""
<tr>
    <td colspan="4" style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="font-weight:bold;font-size:1.9em;">{tekst}</span>
    </td>
</tr>"""
    
    def _html_tabel_kop2(self, tekst):
        return f"""
<tr>
    <td colspan="4" style="text-align:left;vertical-align:top;background-color:#eee;border-top:1px solid #888;border-bottom:1px solid #888;">
        <span style="font-weight:normal;font-size:1.5em;">{tekst}</span>
    </td>
</tr>"""
    
    def _html_tabel_tekst(self, naam, tekst, docu):
        klasse_naam, naam = self._vervang_naam(naam)
        
        if naam == '' and docu == '':
            return f"""
<tr>
    <td colspan="4" style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{tekst}</span>
    </td>
</tr>"""
        elif naam == '':
            return f"""
<tr>
    <td colspan="3" style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{tekst}</span>
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;">
        <span style="">{docu}</span>
    </td>
</tr>"""
        elif docu == '':
            return f"""
<tr>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">${naam}$</span>
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{self._html_spacer(1, 1)}</span>
    </td>
    <td colspan="2" style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{tekst}</span>
    </td>
</tr>"""
        else:
            return f"""
<tr>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">${naam}$</span>
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{self._html_spacer(1, 1)}</span>
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span style="">{tekst}</span>
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;">
        <span style="">{docu}</span>
    </td>
</tr>"""
    
    def _html_tabel_figuur(self, naam, obj):
        klasse_naam, naam = self._vervang_naam(naam)
        naam = '$' + naam + '$' if naam != '' else '&nbsp;'
        
        return f"""
<tr>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">{naam}</td>
    <td colspan="3" style="text-align:center;vertical-align:top;background-color:#fff;">{obj.png_html}</td>
</tr>"""
        
    def _html_tabel_waarde(self, naam, obj, docu):
        klasse_naam, naam = self._vervang_naam(naam)
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
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span>{_1}</span>
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;">
        <span>{_2}</span>
    </td>
    <td style="text-align:left;vertical-align:top;background-color:#fff;">
        <span>{_3}</span>
    </td>
    <td style="text-align:right;vertical-align:top;background-color:#fff;">
        <span>{_4}</span>
    </td>
</tr>"""
        
    @property
    def html(self):
        html = ''
        
        html += self._html_tabel_start()
        
        if self._titel is not None:
            html += self._html_tabel_kop1(self._titel)
        
        for typ, naam, obj, docu in self._onderdelen:
            if typ == self.TYPE_TEKST:
                html += self._html_tabel_tekst(naam, obj, docu)
            elif typ == self.TYPE_KLASSE_START:
                html +=  self._html_tabel_lege_regel()
                html +=  self._html_tabel_kop2(naam)
            elif typ == self.TYPE_KLASSE_EINDE:
                html += self._html_tabel_lijn()
            elif typ == self.TYPE_FUNCTIE:
                pass
            elif typ == self.TYPE_WAARDE:
                html += self._html_tabel_waarde(naam, obj, docu)
            elif typ == self.TYPE_FIGUUR:
                html += self._html_tabel_figuur(naam, obj)
            elif typ == self.TYPE_PYCO_OVERIG:
                pass
        
        html += self._html_tabel_einde()
        
        return html