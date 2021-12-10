from pyco.interface import Document

doc = Document()
fn = doc.functies
x = doc.model.Waarde

print('Voorbeeld uit de cursus Wiskunde in de Civiele Techniek N1')

# compactheid van kubus

b1 = x(13).cm
b2 = x(184).mm
b3 = x(22).cm

def compactheid_kubus(b):
    V = fn.V_kubus(b)
    A = fn.A_kubus(b)
    c = (V / A).cm
    return c

def norm_compactheid_kubus(b):
    c = compactheid_kubus(b)
    V_s = x(36*fn.pi).m3
    V = fn.V_kubus(b)
    k = fn.macht(float(V_s / V), 1/3)
    n = (c * k).cm
    return n

print()
frmt_compactheid = 'compactheid kubus b  = {} --> {}'
print(frmt_compactheid.format(b1, compactheid_kubus(b1)))
print(frmt_compactheid.format(b2, compactheid_kubus(b2)))
print(frmt_compactheid.format(b3, compactheid_kubus(b3)))

print()
frmt_genorm_compactheid = 'genormeerde compactheid kubus b  = {} --> {}'
print(frmt_genorm_compactheid.format(b1, norm_compactheid_kubus(b1)))
print(frmt_genorm_compactheid.format(b2, norm_compactheid_kubus(b2)))
print(frmt_genorm_compactheid.format(b3, norm_compactheid_kubus(b3)))
