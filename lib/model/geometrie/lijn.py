import pyco.model as pycom


class Lijn(pycom.BasisObject):

    def __init__(self, knoop1=None, knoop2=None):
        super().__init__()

        self._knoop1 = None
        self._knoop2 = None

        self.knoop1 = knoop1
        self.knoop2 = knoop2

    @property
    def knoop1(self):
        return self._knoop1

    @knoop1.setter
    def knoop1(self, knoop1):
        if knoop1 is not None:
            if not isinstance(knoop1, pycom.Knoop):
                raise TypeError('knoop1 is geen type Knoop')
            self._knoop1 = knoop1

    @property
    def knoop2(self):
        return self._knoop2

    @knoop2.setter
    def knoop2(self, knoop2):
        if knoop2 is not None:
            if not isinstance(knoop2, pycom.Knoop):
                raise TypeError('knoop2 is geen type Knoop')
            self._knoop2 = knoop2

    def __repr__(self):
        return 'Lijn(knoop1={!r}, knoop2={!r})'.format(self.knoop1, self.knoop2)

    def __str__(self):
        return '{!s} --> {!s}'.format(self.knoop1, self.knoop2)
