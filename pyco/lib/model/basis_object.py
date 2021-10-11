import pyco.basis as pycob

class BasisObject(object):
    """Deze klasse dient als onderlegger voor alle klassen."""

    def __init__(self):
        self._documentatie = ''

        # ObjectTeller zorgt ervoor dat over hele applicatie objecten een nieuw
        # oplopend nummer krijgen. Hierdoor kan achteraf gekeken worden welk object
        # eerder was aangemaakt.
        teller = pycob.ObjectTeller()
        self._object_nummer = teller.object_nummer

    def __rshift__(self, other:str):
        """Documentatie toevoegen.

        Object() >> "Documentatie."
        """
        self._documentatie = other.strip() if isinstance(other, str) else ''
        return self

    @classmethod
    def print_help(cls):
        name = cls.__name__
        underline = '+--' + len(name)*'-' + '--+'
        docstr = ''
        for line in cls.__doc__.split('\n'):
            line = line[4:] if line[:4] == '    ' else line
            docstr += line + '\n'
        fstr = f"\n{underline}\n|  {name}  |\n{underline}\n{docstr}"
        print(fstr)
