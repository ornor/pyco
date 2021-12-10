from pyco.interface import Document

doc = Document()
fn = doc.functies
x = doc.model.Waarde

# ==============================================

L = x(3).m
b = x(200).mm
h = x(400).mm

materiaal = 'hout'

F = x(20).kN
q = x(100).kN_m

# ==============================================

MATERIALEN = {
    'staal': {
         'E': x(210000).N_mm2,
         'f_d': x(235).N_mm2,
    },
    'hout': {
         'E': x(1100).N_mm2,
         'f_d': x(14).N_mm2,
    },
    'beton': {
         'E': x(30000).N_mm2,
         'f_d': x(25).N_mm2,
    },
}

E = MATERIALEN[materiaal]['E']
f_d = MATERIALEN[materiaal]['f_d']

A = b * h
I = 1/12 * b * h**3
W = 1/6 * b * h**2

F_opleg_F = 1/2 * F
F_opleg_q = 1/2 * q * L
F_opleg = F_opleg_F + F_opleg_q

M_max_F = 1/4 * F * L
M_max_q = 1/8 * q * L**2
M_max = M_max_F + M_max_q
sigma_max = M_max / W

w_max_F = 1/12 * M_max_F * L**2 / (E * I)
w_max_q = 5/48 * M_max_q * L**2 / (E * I)
w_max = w_max_F + w_max_q

print('optredende spanning: {:.1f}'.format(sigma_max.N_mm2))
print('opneembare spanning: {:.1f}'.format(f_d.N_mm2))

if sigma_max <= f_d:
    print('in orde!')
else:
    print('voldoet NIET')

print('oplegreactie links/rechts: {:.0f}'.format(F_opleg.kN))
print('maximale doorbuiging: {:.1f}'.format(w_max.mm))
