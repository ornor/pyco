import pyco.model as pycom


class Lijn(pycom.BasisObject):

    def __init__(self, *knopen):
        super().__init__()

        self._knopen = []
        self._eenheid = None

        if len(knopen) == 1 and (isinstance(knopen[0], list) or
                                 isinstance(knopen[0], tuple)):
            knopen = knopen[0]

        if len(knopen) < 2:
            raise ValueError('een lijn bestaat uit minimaal twee knopen')

        for i, knoop in enumerate(knopen):
            if isinstance(knoop, pycom.Knoop):
                if i > 0:
                    if ((self._eenheid is None and knoop.eenheid is not None)
                            or (self._eenheid is not None and knoop.eenheid is None)):
                        raise ValueError('knopen moeten zelfde type eenheid hebben')
                    knoop.eenheid = self._eenheid
                if i == 0 or (i > 0 and self._knopen[-1] != knoop):
                    self._knopen.append(knoop)
            elif isinstance(knoop, list) or isinstance(knoop, tuple):
                knoop = pycom.Knoop(knoop)
                if i > 0:
                    if ((self._eenheid is None and knoop.eenheid is not None)
                        or (self._eenheid is not None and knoop.eenheid is None)):
                        raise ValueError('knopen moeten zelfde type eenheid hebben')
                    knoop.eenheid = self._eenheid
                if i == 0 or (i > 0 and self._knopen[-1] != knoop):
                    self._knopen.append(knoop)
            else:
                raise TypeError('opgegeven argument is geen Knoop object of lijst met getallen/Waardes')
            if i == 0:
                self._eenheid = knoop.eenheid

    @property
    def eenheid(self):
        """Geeft eenheid van Waarde. 'None' als geen eenheid."""
        return self._eenheid

    @eenheid.setter
    def eenheid(self, eenheid:str):
        """Zet knopen om naar nieuwe eenheid."""
        for k in self:
            k.eenheid = eenheid
        self._eenheid = eenheid

    def __eq__ (self, andere):
        if len(self) != len(andere):
            return False
        return all(s == a for s, a in zip(self, andere))

    def __neq__ (self, andere):
        return not self == andere

    def __iter__(self):
        return (k for k in self._knopen)

    def __getitem__(self, index):
        return self._knopen[index]

    def __len__(self):
        return len(self._knopen)

    def __format__(self, config:str=None):
        """Geeft tekst met geformatteerd getal en eenheid."""
        if config is None:
            return str(self)
        knopen = ', '.join(format(k, config).rsplit(')', 1)[0]+')' for k in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(knopen, eenheid).strip()

    def __repr__(self):
        cls_naam = type(self).__name__
        knopen = ', '.join(repr(k) for k in self)
        return '{}({})'.format(cls_naam, knopen)

    def __str__(self):
        knopen = ', '.join(str(k).rsplit(')', 1)[0]+')' for k in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(knopen, eenheid).strip()
