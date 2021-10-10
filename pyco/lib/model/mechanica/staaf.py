import pyco.model as pycom


class Staaf(pycom.BasisObject):
    
    def __init__(self, lijn=None):
        super().__init__()
        
        self._lijn = None
        
        self.lijn = lijn
        
    @property
    def lijn(self):
        return self._lijn
    
    @lijn.setter
    def lijn(self, lijn):
        if lijn is not None:
            if not isinstance(lijn, pycom.Lijn):
                raise TypeError('lijn is geen type Lijn')
            self._lijn = lijn
        
    def __repr__(self):
        return 'Staaf(lijn={!r})'.format(self.lijn)
    
    def __str__(self):
        return '{!s}'.format(self.lijn)