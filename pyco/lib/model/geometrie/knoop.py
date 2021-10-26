import pyco.model as pycom

class Knoop(pycom.BasisObject):

    def __init__(self, x=None, y=None, z=None):
        super().__init__()
        self._x = None
        self._y = None
        self._z = None

    def _controleer_waarde(self, naam, waarde):
        if not isinstance(waarde, pycom.Waarde):
            raise ValueError('waarde \'{}\' is geen geldige Waarde'.format(naam))
        # TODO controleer of eenheidbreuk LENGTE is

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        if x is not None:
            self._controleer_waarde('x', x)
            self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        if y is not None:
            self._controleer_waarde('y', y)
            self._y = y

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, z):
        if z is not None:
            self._controleer_waarde('z', z)
            self._z = z

    def __repr__(self):
        return 'Knoop({}, {}, {})'.format(self.x if self.x is not None else '',
                                   self.y if self.y is not None else '',
                                   self.z if self.z is not None else '')

    def __str__(self):
        return '({},{},{})'.format(self.x if self.x is not None else '',
                                   self.y if self.y is not None else '',
                                   self.z if self.z is not None else '')
