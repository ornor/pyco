from pyco.interface import Document

doc = Document()
x = doc.model.Waarde

b = x(23).cm._0
print('b', b)

h = x(341).mm
print('h', h)

A = b * h
print('A', A)

F = x(803)['kN'][0]
print('F', F)

sigma = (F / A).N_mm2._1
print('sigma', sigma)
print(sigma('kN/mm2'))
