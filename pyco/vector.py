from typing import Union
import itertools
import numpy as np

import pyco.basis
import pyco.waarde

class pc:
    BasisObject = pyco.basis.BasisObject
    Waarde = pyco.waarde.Waarde

class Vector(pc.BasisObject):
    """
    Bevat een lijst van getallen of Waarde objecten met allen dezelfde eenheid.

    AANMAKEN VECTOR             eenheid van 1e component, geldt voor geheel
        v = Vector([waarde1, waarde2, waarde3])

    AANPASSEN EENHEID           omzetten van eenheid naar andere eenheid
        v.eenheid               huidige eenheid opvragen (tekst of None)
        v.eenheid = 'N/mm2'     eenheid aanpassen
        v.gebruik_eenheid('m')  zelfde als bovenstaande, retourneert object

    OMZETTEN VECTOR NAAR TEKST  resulteert in nieuw string object
        tekst = str(v)          of automatisch met bijvoorbeeld print(w)
        tekst = format(v,'.2f') format configuratie meegeven voor getal

    MOGELIJKE BEWERKINGEN       resulteert in nieuw Vector object
        v3 = v1 + v2            vector optellen bij vector
        v3 = v1 - v2            vector aftrekken van vector
        getal = v1 * v2         vector vermenigvuldigen met vector (inproduct)
        getal = v1 / v2         vector delen door vector (inverse inproduct)
        v2 = n * v1             getal vermenigvuldigen met vector
        v2 = v1 * n             vector vermenigvuldigen met getal
        v2 = n / v1             getal delen door vector
        v2 = v1 / n             vector delen door getal
        waarde = v1 ** n        vector tot de macht een geheel getal
        waarde = abs(v1)        berekent lengte van vector -> Waarde object
        getal = float(v1)       berekent lengte van vector -> float object
        v2 = +v1                behoud teken
        v2 = -v1                verander teken (positief vs. negatief)
        for w in v1:            itereert en geeft float/Waarde object terug
        getal = len(v1)         geeft aantal elementen (dimensies) van vector

    NUMPY BEWERKINGEN           gebruikt array object
        numpy_array = v1.array  retourneert Numpy array object
                                    (bevat allen getallen, zonder eenheid)
        getal = v1[2]           retourneert getal (zonder eenheid) op index
        numpy_array = v1[1:3]   retourneert Numpy array object vanuit slice

    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        v1 == v2                is gelijk aan
        v1 != v2                is niet gelijk aan
        v1 >  v2                de lengte van vector is groter dan
        v1 <  v2                de lengte van vector is kleiner dan
        v1 >= v2                de lengte van vector is groter dan of gelijk aan
        v1 <= v2                de lengte van vector is kleiner dan of gelijk aan
        v1 &  v2                eenheden zijn zelfde type
    """

    def __init__(self, *waardes:Union[pc.Waarde, int, float]):
        super().__init__()

        self._eenheid = None
        tmp_waardes = []

        if len(waardes) < 1:
            raise ValueError('Er moet minimaal één waarde worden opgegeven.')

        if len(waardes) == 1 and \
                (isinstance(waardes[0], list) or isinstance(waardes[0], tuple)):
            waardes = waardes[0]

        for i, waarde in enumerate(waardes):
            if i == 0:
                # eerste waarde
                if isinstance(waarde, pc.Waarde):
                    _, eenheid = tuple(waarde)
                    if eenheid != '':
                        self._eenheid = eenheid
            else:
                # volgende waardes
                if isinstance(waarde, pc.Waarde):
                    # check of type eenheid zelfde is
                    if not waarde & pc.Waarde(1, self._eenheid):
                        raise TypeError('type eenheid komt niet overeen met 1e waarde: {}'.format(waarde))
                    # eenheden omzetten naar eerste eenheid
                    waarde = waarde[self._eenheid]
                elif isinstance(waarde, float) or isinstance(waarde, int):
                    if self._eenheid is not None:
                        raise TypeError('type eenheid komt niet overeen met 1e waarde: {}'.format(waarde))
            # waardes toevoegen aan self._array
            if isinstance(waarde, pc.Waarde):
                getal, _ = tuple(waarde)
                if isinstance(getal, float) or isinstance(getal, int):
                    tmp_waardes.append(getal)
                else:
                    raise TypeError('waarde in Waarde object is geen getal')
            elif isinstance(waarde, float) or isinstance(waarde, int):
                tmp_waardes.append(float(waarde))
            else:
                raise TypeError('waarde is geen Waarde/float/int: {}'.format(waarde))

        self._array = np.array(tmp_waardes, dtype='float64')

    @property
    def eenheid(self):
        """Geeft eenheid van Waarde. 'None' als geen eenheid."""
        return self._eenheid

    @eenheid.setter
    def eenheid(self, eenheid:str):
        """Zet Vector om naar nieuwe eenheid."""
        if self._eenheid is None:
            self._eenheid = eenheid
        else:
            tmp_waardes = []
            oude_eenheid = self._eenheid
            for w in self:
                w = float(pc.Waarde(float(w), oude_eenheid)[eenheid])
                tmp_waardes.append(w)
            self._array = np.array(tmp_waardes, dtype='float64')
            self._eenheid = eenheid

    def gebruik_eenheid(self, eenheid:str):
        """Zet om naar nieuwe eenheid en retourneert object."""
        self.eenheid = eenheid
        return self

    @property
    def array(self):
        """Retourneert Numpy array object met alle getallen (zonder eenheid)."""
        return self._array

    def __add__(self, andere):
        """Telt waarden bij elkaar op."""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        pairs = itertools.zip_longest(self, andere, fillvalue=0.0)
        cls = type(self)
        return cls([a + b for a, b in pairs])

    def __sub__(self, andere):
        """Trekt waarde van elkaar af"""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        pairs = itertools.zip_longest(self, andere, fillvalue=0.0)
        cls = type(self)
        return cls([a - b for a, b in pairs])

    def __mul__(self, andere):
        """Vermenigvuldigd Vector met andere Vector (inproduct) of scalar getal."""
        if isinstance(andere, Vector):
            pairs = itertools.zip_longest(self, andere, fillvalue=0.0)
            for i, (a, b) in enumerate(pairs):
                if i == 0:
                    product = a * b
                else:
                    product += a * b
            return product
        elif isinstance(andere, int) or isinstance(andere, float):
            cls = type(self)
            return cls([w * andere for w in self])
        else:
            raise TypeError('tweede waarde is geen Vector object of getal')

    #def __matmul__(self, andere):
    #    @ operator -> gebruiken voor kruisproduct? (en niet inproduct); vanaf python 3.5

    def __truediv__(self, andere):
        """Deelt Vector met andere Vector (inproduct) of scalar getal."""
        if isinstance(andere, Vector):
            pairs = itertools.zip_longest(self, andere, fillvalue=0.0)
            for i, (a, b) in enumerate(pairs):
                if i == 0:
                    product = (a / b)
                else:
                    product += (a / b)
            return product
        elif isinstance(andere, int) or isinstance(andere, float):
            cls = type(self)
            return cls([w / andere for w in self])
        else:
            raise TypeError('tweede waarde is geen Vector object of getal')

    def __pow__(self, macht):
        """Doet Vector tot de macht een geheel getal > 1."""
        if isinstance(macht, int) and macht > 1:
            resultaat = self
            for i in range(2, macht+1):
                resultaat = resultaat * resultaat
            return resultaat
        else:
            raise ValueError('macht moet geheel getal zijn groter dan 1')

    def __rmul__(self, andere):
        """Vermenigvuldigd scalar getal met Vector."""
        return self * andere

    def __rtruediv__(self, andere):
        """Deelt scalar met eenheidsloze Vector."""
        if (isinstance(andere, int) or isinstance(andere, float)) and \
                self.eenheid is None:
            cls = type(self)
            return cls([andere / w for w in self])
        else:
            raise TypeError('kan alleen getal delen door eenheidsloze Vector')

    def __eq__(self, andere):
        """Vergelijkt Vector met andere Vector."""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        if len(self) != len(andere):
            return False
        if self.eenheid is None and andere.eenheid is not None:
            return False
        if self.eenheid is not None and andere.eenheid is None:
            return False
        if not W(1, self.eenheid) & W(1, andere.eenheid):
            # ander type eenheid
            return False
        for w1, w2 in zip(self, andere):
            if self.eenheid is None:
                # w is float object
                if round(w1*pc.Waarde._AFRONDEN_BIJ_VERGELIJKEN) != round(w2*pc.Waarde._AFRONDEN_BIJ_VERGELIJKEN):
                    return False
            else:
                # w is Waarde object
                if w1 != w2:
                    return False
        return True

    def __neq__(self, andere):
        """Vergelijkt Vector negatief met andere Vector"""
        return not self.__eq__(andere)

    def __lt__(self, andere):
        """Kijkt of absolute waarde (lengte vector) kleiner is dan andere Vector."""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        if len(self) != len(andere):
            raise TypeError('tweede vector heeft niet zelfde dimensie')
        if self.eenheid is None and andere.eenheid is not None:
            raise TypeError('tweede vector heeft niet zelfde eenheid')
        if self.eenheid is not None and andere.eenheid is None:
            raise TypeError('tweede vector heeft niet zelfde eenheid')
        if not pc.Waarde(1, self.eenheid) & pc.Waarde(1, andere.eenheid):
            raise TypeError('tweede vector heeft niet zelfde type eenheid')
        return abs(self) < abs(andere)

    def __gt__(self, andere):
        """Kijkt of absolute waarde (lengte vector) groter is dan andere Vector."""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        if len(self) != len(andere):
            raise TypeError('tweede vector heeft niet zelfde dimensie')
        if self.eenheid is None and andere.eenheid is not None:
            raise TypeError('tweede vector heeft niet zelfde eenheid')
        if self.eenheid is not None and andere.eenheid is None:
            raise TypeError('tweede vector heeft niet zelfde eenheid')
        if not pc.Waarde(1, self.eenheid) & pc.Waarde(1, andere.eenheid):
            raise TypeError('tweede vector heeft niet zelfde type eenheid')
        return abs(self) > abs(andere)

    def __le__(self, andere):
        """Kijkt of absolute waarde (lengte vector) kleiner dan of gelijk is aan andere Vector."""
        if self.__lt__(andere):
            return True
        else:
            return abs(self) == abs(andere)

    def __ge__(self, andere):
        """Kijkt of absolute waarde (lengte vector) groter dan of gelijk is aan andere Vector."""
        if self.__gt__(andere):
            return True
        else:
            return abs(self) == abs(andere)

    def __and__(self, andere):
        """Controleert of Vector zelfde type eenheid heeft als andere."""
        if not isinstance(andere, Vector):
            raise TypeError('tweede waarde is geen Vector object')
        return pc.Waarde(1, self.eenheid) & pc.Waarde(1, andere.eenheid)

    def __float__(self):
        """Berekent de lengte van de vector als float object."""
        return np.linalg.norm(self.array)

    def __abs__(self):
        """Berekent de lengte van de vector als Waarde object."""
        return pc.Waarde(float(self), self.eenheid)

    def __pos__(self):
        """Behoud teken (positief = positief, negatief = negatief)."""
        self._array *= 1  # moet met underscore
        return self

    def __neg__(self):
        """Verander teken (positief = negatief, negatief = postief)."""
        self._array *= -1  # moet met underscore
        return self

    def __bool__(self):
        """Geeft False als lengte Vector == 0. Anders True."""
        length = float(self)
        return not (length < 1/W._AFRONDEN_BIJ_VERGELIJKEN and length > -1/W._AFRONDEN_BIJ_VERGELIJKEN)

    def __iter__(self):
        """Itereert over waardes. Als geen eenheid: floats. Als wel eenheid dan Waarde objecten."""
        eenheid = self.eenheid
        for w in self.array:
            if eenheid is None:
                yield w
            else:
                yield pc.Waarde(w, eenheid)

    def __len__(self):
        """Geeft aantal dimensies (waarden) van vector."""
        return len(self.array)

    def __format__(self, config:str=None):
        """Geeft tekst met geformatteerd getal en eenheid."""
        if config is None:
            return str(self)
        format_str = '{:' + config + '}'
        waardes = ', '.join(format_str.format(float(w)) for w in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(waardes, eenheid).strip()

    def __repr__(self):
        """Geeft representatie object."""
        cls_naam = type(self).__name__
        if self.eenheid is None:
            waardes = ', '.join(str(float(w)) for w in self)
        else:
            waardes = ', '.join(repr(pc.Waarde(float(w), self.eenheid)) for w in self)
        return '{}({})'.format(cls_naam, waardes)

    def __str__(self):
        """Geeft tekst met vector en eenheid"""
        waardes = ', '.join(str(float(w)) for w in self)
        eenheid = self.eenheid if self.eenheid is not None else ''
        return '({}) {}'.format(waardes, eenheid).strip()

    def __getitem__(self, subset):
        """Geeft subset van numpy array met waarden."""
        return self.array[subset]

        # """Retourneer subset van waardes (floats of Waarde objecten).
        # Als slice dan wordt er nieuw Vector object gegenereert"""
        # waardes = [w for w in self]
        # if isinstance(subset, int):
        #     return waardes[subset]
        # elif isinstance(subset, slice):
        #     cls = type(self)
        #     return cls(waardes[subset])
        # else:
        #     raise TypeError('index moet geheel getal of slice zijn')
