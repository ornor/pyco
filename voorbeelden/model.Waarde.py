from pyco.interface import Document
import pyco.functies as fn

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
print('spanning heeft waarde getal (kN/mm2):', float(sigma['kN/mm2']))

# ps. waardes worden intern NOOIT afgerond; alleen bij omzetten naar tekst


print()
# waardes vergelijken
r = x(23).mm
s = x(2.3).cm
t = x(5).m

print('r == s   -->   {} == {}   -->  '.format(r, s), r == s)
print('r != t   -->   {} != {}    -->  '.format(r, t), r != t)
print('s > t    -->    {} >  {}    -->  '.format(s, t), s > t)
print('s <= t   -->    {} <= {}    -->  '.format(s, t), s <= t)


print()
# pyco functies zijn geschikt voor Waarde objecten
r = x(20).mm
h = x(10).cm

print('V bol:', fn.V_bol(r).cm3)
print('V kegel:', fn.V_kegel(r, h).cm3)

print('A hele cirkel:', fn.A_cirkel(r).cm2)
alpha = x(45).deg
print('A cirkelsegment:', fn.A_cirkelsegment(alpha, r).cm2)


if False:
    # hieronder staan nog extra opties
    doc.model.Waarde.print_help()
