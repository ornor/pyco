from pyco.interface import Document

doc = Document()
x = doc.model.Waarde

# aanmaken waarde met eenheid als tekst
b = x(23, 'cm')
print('b =', b)

# aanmaken waarde met dimensieloze eenheid
# vervolgens omzetten naar (standaard) eenheid via aanroepen eigenschap
# tevens waarde standaard laten afronden (pas bij uitvoer) naar 0 decimalen
h = x(341).mm._0
print('h =', h)

# rekenen met waardes (in dit geval vermenigvuldigen)
# de waarde kiest nu zelf een nieuwe standaard eenheid (in dit geval m2)
A = b * h
print('A =', A, '(v1)')

# aangeven dat standaard uitvoer in mm2 moet worden getoond
A = A.mm2
print('A =', A, '(v2)')

# aangeven dat standaard uitvoer afgerond moet worden op 0 decimalen
A = A._0
print('A =', A, '(v3)')

# aanmaken waarde met dimensieloze eenheid
# vervolgens omzetten naar een eenheid via opgeven van tekst (vierkantie haken)
# tevens waarde standaard laten afronden (pas bij uitvoer) naar 0 decimalen
#   door opgeven van een geheel getal (vierkante haken)
F = x(803)['kN'][0]
print('F =', F)

# aanmaken waarde
sigma = (F / A).N_mm2._1
print('sigma =', sigma)

# waarde omzetten naar een getal (float); door ronde haken met eenheid tekst
# met een getal kan je ook rekenen met niet standaard functies zoals math.sin()
print('spanning heeft getal (kN/mm2):', sigma('kN/mm2'))


# =============================================================================


"""
AANMAKEN WAARDE
    w = Waarde(getal)
    w = Waarde(getal, eenheid_tekst)

AANPASSEN EENHEID           (pas wanneer waarde wordt getoond als tekst)
    w = w['mm']
    w = w.mm                (kan voor standaard eenheden)

AANPASSEN AFRONDING         (pas wanneer waarde wordt getoond als tekst)
    w = w[0]
    w = w._0                (kan voor 0 t/m 9)

OMZETTEN WAARDE NAAR TEKST
    tekst = str(w)

OMZETTEN WAARDE NAAR GETAL  (float object)
    getal = w('cm')

"""
