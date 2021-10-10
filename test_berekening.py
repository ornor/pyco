from pyco.interface import Document

doc = Document()

h = doc.x(12).mm(4)
b = doc.x(34, 'cm')

A = h*b

print(h)
print(A.mm2(8))
