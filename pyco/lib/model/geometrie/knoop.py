import pyco.model as pycom

class Knoop(pycom.Vector):
    """
    Bevat een lijst van getallen of Waarde objecten (met een lengte eenheid).

    AANMAKEN KNOOP              eenheid van 1e component, geldt voor geheel
        k = Knoop([waarde1, waarde2, waarde3])

    AANPASSEN EENHEID           omzetten van eenheid naar andere eenheid
        k.eenheid               huidige eenheid opvragen (tekst of None)
        k.eenheid = 'N/mm2'     eenheid aanpassen

    OMZETTEN KNOOP NAAR TEKST   resulteert in nieuw string object
        tekst = str(k)          of automatisch met bijvoorbeeld print(w)
        tekst = format(k,'.2f') format configuratie meegeven voor getal

    MOGELIJKE BEWERKINGEN       resulteert in nieuw Knoop object
        k3 = k1 + k2            knoop optellen bij knoop
        k3 = k1 - k2            knoop aftrekken van knoop
        k2 = n * k1             getal vermenigvuldigen met knoop
        k2 = k1 * n             knoop vermenigvuldigen met getal
        k2 = n / k1             getal delen door knoop
        k2 = k1 / n             knoop delen door getal
        k2 = +k1                behoud teken
        k2 = -k1                verander teken (positief vs. negatief)
        Waarde/getal = k1[3]    retourneert float/Waarde object op index
        Waarde/getal = k1.x     retourneert 1e element
        Waarde/getal = k1.y     retourneert 2e element
        Waarde/getal = k1.z     retourneert 3e element
        getal = len(k1)         geeft aantal elementen (dimensies) van knoop

    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        k1 == k2                is gelijk aan
        k1 != k2                is niet gelijk aan
        k1 &  k2                eenheden zijn zelfde type
    """

    def __init__(self, *waardes):
        super().__init__(*waardes)

        if not (self.eenheid is None
                or pycom.Waarde(1, self.eenheid) & pycom.Waarde(1, 'm')):
            raise ValueError('eenheid van waardes is geen lengte-eenheid')

    @property
    def x(self):
        """Retourneert 1e element."""
        if len(self) > 0:
            return self[0]
        else:
            raise IndexError('knoop heeft geen elementen')

    @property
    def y(self):
        """Retourneert 2e element."""
        if len(self) > 1:
            return self[1]
        else:
            raise IndexError('knoop heeft minder dan twee elementen')

    @property
    def z(self):
        """Retourneert 3e element."""
        if len(self) > 2:
            return self[2]
        else:
            raise IndexError('knoop heeft minder dan drie elementen')
