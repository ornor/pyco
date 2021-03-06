import pyco.model as pycom

import webbrowser
import tempfile
import os.path

class Html(pycom.BasisObject):
    """
    Verzorgt HTML uitvoer.
    """

    def __init__(self):
        super().__init__()

        self.titel = 'PYCO'

        self._doctype= '<!DOCTYPE html>\n'
        self._html_open = '<html lang="nl-NL">\n'
        self._head_open = '<head>\n<meta charset="UTF-8">\n'
        self._title_open = '<title>'
        self._title_close = '</title>\n'
        self._head = ''
        self._head_close = '</head>\n'
        self._body_open = '<body>\n'
        self._body = ''
        self._body_close = '</body>\n'
        self._html_close = '</html>\n'

        self._head += """
<style>
    body {font-family:sans-serif; padding:0px;}
    h1 {margin:10px 0px 20px 0px; padding:0px;}
    h2 {margin:5px 0px 10px 0px; padding:0px;}
    pre {margin:5px 0px 20px 0px; padding:0px;}
    p {margin:5px 0px 20px 0px; padding:0px;}
    div {margin:0px; padding:0px;}
</style>
        """.strip() + '\n'

    @property
    def html(self):
        return self._doctype + self._html_open + self._head_open \
            + self._title_open + self.titel + self._title_close \
            + self._head + self._head_close + self._body_open \
            + self._body + self._body_close + self._html_close

    def head(self, html:str):
        self._head += html + '\n'

    def body(self, html:str):
        self._body += html + '\n'

    def openen_in_browser(self):
        html_bestand_adres = os.path.join(tempfile.gettempdir(), 'pyco.html')

        with open(html_bestand_adres, mode='w', encoding='utf-8') as f:
            f.write(self.html)

        new = 2 # openen in nieuw tabblad, daar waar mogelijk
        webbrowser.open('file://' + os.path.realpath(html_bestand_adres), new=new)
