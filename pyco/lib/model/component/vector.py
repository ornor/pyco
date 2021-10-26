from typing import Union

import pyco.model as pycom


class Vector(pycom.BasisComponent):
    """
    Bevat een lijst van getallen (Waarde objecten) met allen dezelfde eenheid.

    AANMAKEN VECTOR             eenheid van 1e component, geldt voor geheel
        v = Vector([waarde1, waarde2, waarde3])


    """

    def __init__(self, *waardes:Union[pycom.Waarde, int, float]):
        super().__init__()

        self._waardes = []
        self._eenheid = None

        for i, waarde in enumerate(waardes):
            if i == 0:
                # eerste waarde
                if isinstance(waarde, pycom.Waarde):
                    _, eenheid = tuple(waarde)
                    if eenheid != '':
                        self._eenheid = eenheid
            else:
                # volgende waardes
                if isinstance(waarde, pycom.Waarde):
                    # check of type eenheid zelfde is
                    if not waarde & pycom.Waarde(1, self._eenheid):
                        raise TypeError('type eenheid komt niet overeen met 1e waarde: {}'.format(waarde))
                    # eenheden omzetten naar eerste eenheid
                    waarde = waarde[self._eenheid]
                elif isinstance(waarde, float) or isinstance(waarde, int):
                    if self._eenheid is not None:
                        raise TypeError('type eenheid komt niet overeen met 1e waarde: {}'.format(waarde))
            # waardes toevoegen aan self._waardes
            if isinstance(waarde, pycom.Waarde):
                getal, _ = tuple(waarde)
                if isinstance(getal, float) or isinstance(getal, int):
                    self._waardes.append(getal)
                else:
                    raise TypeError('waarde in Waarde object is geen getal')
            elif isinstance(waarde, float) or isinstance(waarde, int):
                self._waardes.append(float(waarde))
            else:
                raise TypeError('waarde is geen Waarde/float/int: {}'.format(waarde))

    @property
    def eenheid(self):
        return self._eenheid

    def __add__(self):
        """."""
        pass

    def __sub__(self):
        """."""
        pass

    def __mul__(self):
        """."""
        pass

    def __truediv__(self):
        """."""
        pass

    def __pow__(self):
        """."""
        pass

    def __rmul__(self):
        """."""
        pass

    def __rtruediv__(self):
        """."""
        pass

    def __eq__(self):
        """."""
        pass

    def __neq__(self):
        """."""
        pass

    def __lt__(self):
        """."""
        pass

    def __gt__(self):
        """."""
        pass

    def __le__(self):
        """."""
        pass

    def __ge__(self):
        """."""
        pass

    def __and__(self):
        """."""
        pass

    def __float__(self):
        """."""
        pass

    def __abs__(self):
        """."""
        pass

    def __pos__(self):
        """."""
        pass

    def __neg__(self):
        """."""
        pass

    def __bool__(self):
        """."""
        pass

    def __iter__(self):
        """Itereert over waardes"""
        return (w for w in self._waardes)

    def __len__(self):
        """."""
        pass

    def __format__(self):
        """."""
        pass

    def __repr__(self):
        """Geeft representatie object."""
        if self._eenheid is None:
            waardes = ', '.join(str(w) for w in self)
        else:
            waardes = ', '.join(repr(pycom.Waarde(w, self._eenheid)) for w in self)
        return 'Vector({})'.format(waardes)

    def __str__(self):
        """Geeft tekst met vecotr en eenheid"""
        waardes = ', '.join(str(w) for w in self)
        eenheid = self._eenheid if self._eenheid is not None else ''
        return '[{}] {}'.format(waardes, eenheid).strip()

    def __getitem__(self):
        """."""
        pass
