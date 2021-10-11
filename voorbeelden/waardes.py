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
A = b * h
print('A =', A)

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
