from pyco.model import Waarde

from typing import Union

import math

# inherit functions of math module
plafond = math.ceil
#comb = math.comb
teken = math.copysign
fabs = math.fabs
factoriaal = math.factorial
vloer = math.floor
fmod = math.fmod
frexp = math.frexp
fsom = math.fsum
gcd = math.gcd
is_gesloten = math.isclose
is_eindig = math.isfinite
is_oneindig = math.isinf
is_nan = math.isnan
ldexp = math.ldexp
modf = math.modf
rest = math.remainder
trunc = math.trunc
exp = math.exp
expm1 = math.expm1
log = math.log
log1p = math.log1p
log10 = math.log10
macht = math.pow
wortel = math.sqrt
acos = math.acos
asin = math.asin
atan = math.atan
atan2 = math.atan2
cos = math.cos
sin = math.sin
tan = math.tan
acosh = math.acosh
asinh = math.asinh
atanh = math.atanh
cosh = math.acosh
sinh = math.sinh
tanh = math.tanh
hypot = math.hypot
graden = math.degrees
radialen = math.radians
erf = math.erf
erfc = math.erfc
gamma = math.gamma
lgamma = math.lgamma
pi = math.pi
e = math.e
tau = math.tau
inf = math.inf
nan = math.nan


def A_vierkant(b:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van vierkant."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return b**2
    else:
        return float(b)**2

assert A_vierkant(b=2) == 4.0
assert A_vierkant(b=Waarde(2).cm) == Waarde(400).mm2


def O_vierkant(b:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van vierkant."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return 4*b
    else:
        return 4*float(b)

assert O_vierkant(b=2) == 8.0
assert O_vierkant(b=Waarde(2).cm) == Waarde(80).mm


def A_rechthoek(b:Union[Waarde, int, float],
                h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van rechthoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return b*h
    else:
        return float(b)*float(h)

assert A_rechthoek(b=2, h=3) == 6.0
assert A_rechthoek(b=Waarde(2).cm, h=3) == 6.0
assert A_rechthoek(b=Waarde(2).cm, h=Waarde(30).mm) == Waarde(600).mm2


def O_rechthoek(b:Union[Waarde, int, float],
                h:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van rechthoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return 2*b + 2*h
    else:
        return 2*float(b) + 2*float(h)

assert O_rechthoek(b=2, h=3) == 10.0
assert O_rechthoek(b=Waarde(2).cm, h=3) == 10.0
assert O_rechthoek(b=Waarde(2).cm, h=Waarde(30).mm) == Waarde(100).mm


def A_driehoek(b:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van driehoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return 1/2*b*h
    else:
        return 1/2*float(b)*float(h)

assert A_driehoek(b=2, h=3) == 3.0
assert A_driehoek(b=Waarde(2).cm, h=3) == 3.0
assert A_driehoek(b=Waarde(2).cm, h=Waarde(30).mm) == Waarde(300).mm2


def A_cirkel(r:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van cirkel."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return pi*r**2
    else:
        return pi*float(r)**2

def A_cirkelsegment(alpha:Union[Waarde, int, float],
                    r:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van cirkelsegment."""
    if all(isinstance(obj, Waarde) for obj in [alpha, r]):
        return alpha / Waarde(2*pi).rad *pi*r**2
    else:
        return 1/2*float(alpha)*float(r)**2

def O_cirkel(r:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van cirkel."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return 2*pi*r
    else:
        return 2*pi*float(r)

def V_prisma(A_grond:Union[Waarde, int, float],
             h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een prisma."""
    if all(isinstance(obj, Waarde) for obj in [A_grond, h]):
        return A_grond*h
    else:
        return float(A_grond)*float(h)

def V_piramide(A_grond:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een piramide."""
    if all(isinstance(obj, Waarde) for obj in [A_grond, h]):
        return 1/3*A_grond*h
    else:
        return 1/3*float(A_grond)*float(h)

def A_cilinder(r:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een cilinder."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return 2*pi*r**2 + 2*pi*r*h
    else:
        return 2*pi*float(r)**2 + 2*pi*float(r)*float(h)

def V_cilinder(r:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een cilinder."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return pi*r**2*h
    else:
        return pi*float(r)**2*float(h)

def V_kegel(r:Union[Waarde, int, float],
            h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een kegel."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return 1/3*pi*r**2*h
    else:
        return 1/3*pi*float(r)**2*float(h)

def A_bol(r:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een bol."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return 4*pi*r**2
    else:
        return 4*pi*float(r)**2

def V_bol(r:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een bol."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return 4/3*pi*r**3
    else:
        return 4/3*pi*float(r)**3

def A_kubus(b:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een kubus."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return 6*b**2
    else:
        return 6*float(b)**2

def V_kubus(b:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een kubus."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return b**3
    else:
        return float(b)**3

def A_balk(b:Union[Waarde, int, float],
           h:Union[Waarde, int, float],
           l:Union[Waarde, int, float],) -> float:
    """Berekent oppervlakte van een balk."""
    if all(isinstance(obj, Waarde) for obj in [b, h, l]):
        return 2*b*h + 2*b*l + 2*h*l
    else:
        return (2*float(b)*float(h) + 2*float(b)*float(l) +
                2*float(h)*float(l))

assert A_balk(b=2, h=3, l=4) == 52.0
assert A_balk(b=Waarde(2).cm, h=3, l=4) == 52.0
assert A_balk(b=Waarde(2).cm, h=Waarde(30).mm, l=Waarde(0.04).m) == Waarde(5200).mm2


def V_balk(b:Union[Waarde, int, float],
           h:Union[Waarde, int, float],
           l:Union[Waarde, int, float],) -> float:
    """Berekent inhoud van een balk."""
    if all(isinstance(obj, Waarde) for obj in [b, h, l]):
        return b*h*l
    else:
        return float(b)*float(h)*float(l)

assert V_balk(b=2, h=3, l=4) == 24.0
assert V_balk(b=Waarde(2).cm, h=3, l=4) == 24.0
assert V_balk(b=Waarde(2).cm, h=Waarde(30).mm, l=Waarde(0.04).m) == Waarde(24).cm3
