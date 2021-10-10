import math

def is_getal(obj):
    return isinstance(obj, int) or isinstance(obj, float)

def is_getal_en_niet_nul(obj):
    return (isinstance(obj, int) or isinstance(obj, float)) and float(obj) != 0.0

def is_tekst(obj):
    return isinstance(obj, str)

def is_tekst_en_niet_leeg(obj):
    return isinstance(obj, str) and obj != ''

def is_lijst_of_tupel(obj):
    return isinstance(obj, list) or isinstance(obj, tuple)

def is_lijst_of_tupel_en_niet_leeg(obj):
    return (isinstance(obj, list) or isinstance(obj, tuple)) and len(obj) > 0

def is_map(obj):
    return isinstance(obj, dict)

def is_map_en_niet_leeg(obj):
    return isinstance(obj, dict) and len(obj) > 0

# inherit functions of math module
ceil = math.ceil
#comb = math.comb
copysign = math.copysign
fabs = math.fabs
factorial = math.factorial
floor = math.floor
fmod = math.fmod
frexp = math.frexp
fsum = math.fsum
gcd = math.gcd
isclose = math.isclose
isfinite = math.isfinite
isinf = math.isinf
isnan = math.isnan
ldexp = math.ldexp
modf = math.modf
#perm = math.perm
#prod = math.prod
remainder = math.remainder
trunc = math.trunc
exp = math.exp
expm1 = math.expm1
log = math.log
log1p = math.log1p
log10 = math.log10
power = math.pow
sqrt = math.sqrt
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
degrees = math.degrees
radians = math.radians
erf = math.erf
erfc = math.erfc
gamma = math.gamma
lgamma = math.lgamma
pi = math.pi
e = math.e
tau = math.tau
inf = math.inf
nan = math.nan
