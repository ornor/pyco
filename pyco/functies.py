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
#perm = math.perm
#prod = math.prod
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
#dist = math.dist
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
        b = float(b)
        return b**2

def O_vierkant(b:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van vierkant."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return 4*b
    else:
        b = float(b)
        return 4*b

def A_rechthoek(b:Union[Waarde, int, float],
                h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van rechthoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return b*h
    else:
        b = abs(b) if isinstance(b, Waarde) else float(b)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return b*h

def O_rechthoek(b:Union[Waarde, int, float],
                h:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van rechthoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return 2*b + 2*h
    else:
        b = abs(b) if isinstance(b, Waarde) else float(b)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return 2*b + 2*h

def A_driehoek(b:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van driehoek."""
    if all(isinstance(obj, Waarde) for obj in [b, h]):
        return b*h/2
    else:
        b = abs(b) if isinstance(b, Waarde) else float(b)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return b*h/2

def A_cirkel(r:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van cirkel."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return pi*r**2
    else:
        r = float(r)
        return pi*r**2

def A_cirkelsegment(alpha:Union[Waarde, int, float],
                    r:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van cirkel segment."""
    if all(isinstance(obj, Waarde) for obj in [alpha, r]):
        return alpha.rad / Waarde(2*pi).rad *pi*r**2
    else:
        alpha = abs(alpha) if isinstance(alpha, Waarde) else float(alpha)
        r = abs(r) if isinstance(r, Waarde) else float(r)
        return 1/2*alpha*r**2

def O_cirkel(r:Union[Waarde, int, float]) -> float:
    """Berekent omtrek van cirkel."""
    if all(isinstance(obj, Waarde) for obj in [r]):
        return 2*pi*r
    else:
        r = float(r)
        return 2*pi*r

def V_prisma(A_grond:Union[Waarde, int, float],
             h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een prisma."""
    if all(isinstance(obj, Waarde) for obj in [A_grond, h]):
        return A_grond*h
    else:
        A_grond = abs(A_grond) if isinstance(A_grond, Waarde) else float(A_grond)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return A_grond*h

def V_piramide(A_grond:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een piramide."""
    if all(isinstance(obj, Waarde) for obj in [A_grond, h]):
        return A_grond*h/3
    else:
        A_grond = abs(A_grond) if isinstance(A_grond, Waarde) else float(A_grond)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return A_grond*h/3

def A_cilinder(r:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een cilinder."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return 2*pi*r**2 + 2*pi*r*h
    else:
        r = abs(r) if isinstance(r, Waarde) else float(r)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return 2*pi*r**2 + 2*pi*r*h

def V_cilinder(r:Union[Waarde, int, float],
               h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een cilinder."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return pi*r**2*h
    else:
        r = abs(r) if isinstance(r, Waarde) else float(r)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return pi*r**2*h

def V_kegel(r:Union[Waarde, int, float],
            h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een kegel."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return pi*r**2*h/3
    else:
        r = abs(r) if isinstance(r, Waarde) else float(r)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return pi*r**2*h/3

def A_bol(r:Union[Waarde, int, float],
          h:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een bol."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return 4*pi*r**2
    else:
        r = abs(r) if isinstance(r, Waarde) else float(r)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return 4*pi*r**2

def V_bol(r:Union[Waarde, int, float],
          h:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een bol."""
    if all(isinstance(obj, Waarde) for obj in [r, h]):
        return pi*r**2*h*4/3
    else:
        r = abs(r) if isinstance(r, Waarde) else float(r)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        return pi*r**2*h*4/3

def A_kubus(b:Union[Waarde, int, float]) -> float:
    """Berekent oppervlakte van een kubus."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return 6*b**2
    else:
        b = float(b)
        return 6*b**2

def V_kubus(b:Union[Waarde, int, float]) -> float:
    """Berekent inhoud van een kubus."""
    if all(isinstance(obj, Waarde) for obj in [b]):
        return b**3
    else:
        b = float(b)
        return b**3

def A_balk(b:Union[Waarde, int, float],
           h:Union[Waarde, int, float],
           l:Union[Waarde, int, float],) -> float:
    """Berekent oppervlakte van een balk."""
    if all(isinstance(obj, Waarde) for obj in [b, h, l]):
        return 2*b*h + 2*b*l + 2*h*l
    else:
        b = abs(b) if isinstance(b, Waarde) else float(b)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        l = abs(l) if isinstance(l, Waarde) else float(l)
        return 2*b*h + 2*b*l + 2*h*l

def V_balk(b:Union[Waarde, int, float],
           h:Union[Waarde, int, float],
           l:Union[Waarde, int, float],) -> float:
    """Berekent inhoud van een balk."""
    if all(isinstance(obj, Waarde) for obj in [b, h, l]):
        return b*h*l
    else:
        b = abs(b) if isinstance(b, Waarde) else float(b)
        h = abs(h) if isinstance(h, Waarde) else float(h)
        l = abs(l) if isinstance(l, Waarde) else float(l)
        return b*h*l
