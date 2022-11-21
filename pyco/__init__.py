# afhankelijke externe bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


###############################################################################


import pyco.basis
BasisObject = pyco.basis.BasisObject

import pyco.waarde
Waarde = pyco.waarde.Waarde

import pyco.lijst
Lijst = pyco.lijst.Lijst

import pyco.knoop
Knoop = pyco.knoop.Knoop

import pyco.lijn
Lijn = pyco.lijn.Lijn

import pyco.vorm
Vorm = pyco.vorm.Vorm

if True:
    import pyco.rechthoek
    Rechthoek = pyco.rechthoek.Rechthoek

    import pyco.cirkel
    Cirkel = pyco.cirkel.Cirkel

import pyco.materiaal
Materiaal = pyco.materiaal.Materiaal


###############################################################################


def functies_print_help():
    print("""
    
+-------------------------------------------+
|  algemene pyco functies en eigenschappen  |
+-------------------------------------------+

ALGEMEEN GEBRUIK VAN FUNCTIES         alle namen met () erachter zijn functies
    pc.wortel(9) == 3.0               direct aan te roepen vanuit pc object
    
ALGEMEEN GEBRUIK VAN EIGENSCHAPPEN
    pc.pi == 3.141592653589793        direct aan te roepen vanuit pc object

WISKUNDIGE FUNCTIES                   (geïmporteerd uit Numpy module)
    invoerwaarden:  int, float, np.array, Waarde of Vector
    sin(x)                            sinus
    cos(x)                            cosinus
    tan(x)                            tangens
    asin(x)                           arcsinus (omgekeerde sin)
    acos(x)                           arccosinus (omgekeerde cos)
    atan(x)                           arctangens (omgekeerde tan)
    hypot(a, b)                       hypotenuse (c in: a^2 + b^c = c^2)
    graden(rad)                       van radialen naar graden
    radialen(deg)                     van graden naar radialen
    sinh(x)                           hyperbolische sinus
    cosh(x)                           hyperbolische cosinus
    tanh(x)                           hyperbolische tangens
    asinh(x)                          arc hyperb. sinus (omgekeerde sinh)
    acosh(x)                          arc hyperb. cosinus (omgekeerde cosh)
    atanh(x)                          arc hyperb. tangens (omgekeerde tanh)
    afronden(x, n)                    rond af op n decimalen (standaard 0)
    plafond(x)                        rond af naar boven (geheel getal)
    vloer(x)                          rond af naar beneden (geheel getal)
    plafond_0_vloer(x)                rond af richting 0 (geheel getal)
    som(lijst)                        de som van de elementen
    product(lijst)                    het product van de elementen
    verschil(lijst)                   lijst met verschillen tussen elementen
    optellen(a, b)                    a + b
    aftrekken(a, b)                   a - b
    vermenigvuldigen(a, b)            a * b
    delen(a, b)                       a / b
    delen_aantal(a, b)                a // b -> afgerond naar beneden
    delen_rest(a, b)                  a % b -> restant na afronden naar beneden
    macht(a, n)                       a ** n
    reciproke(x)                      1 / x
    negatief(x)                       -x
    kruisproduct(a, b)                a x b: staat loodrecht op vector a en b
    inwendigproduct(a, b)             a . b: is |a| * |b| * cos(theta)
    exp(x)                            exponentieel: berekent e^x
    ln(x)                             natuurlijke logaritme (grondgetal e)
    log(x)                            logaritme met grondgetal 10
    kgv(a, b)                         kleinste gemene veelvoud: a=12 b=20: 60
    ggd(a, b)                         grootste gemene deler: a=12 b=20: 4
    min(lijst)                        bepaalt minimum waarde lijst
    max(lijst)                        bepaalt maximum waarde lijst
    bijsnijden(lijst, min, max)       snij alle elementen af tot minmax bereik
    wortel(x)                         vierkantswortel
    wortel3(x)                        kubieke wortel
    abs(x)                            absolute waarde (altijd positief)
    teken(x)                          positief getal: 1.0   negatief: -1.0 
    kopieer_teken(a, b)               neem getal a, met het teken (+-) van b
    is_positief(a, b)                 stap functie:a<0 -> 0, a=0 -> b, a>0 -> 1 
    verwijder_nan(lijst)              verwijder niet-getallen (not a number)
    vervang_nan(lijst)                vervang: nan=0, inf=1.7e+308 (heel groot)
    interp(x, lijst_x, lijst_y)       interpoleer x in y; lijst_x MOET oplopen
    van_totmet_n(van, tot_met, n)     genereert vast aantal getallen (incl. tot)
    van_tot_stap(van, tot, stap)      genereert vaste stappen (excl. tot)
    gemiddelde(lijst)                 bepaalt het gemiddelde
    stdafw_pop(lijst)                 bepaalt standaardafwijking voor populatie
    stdafw_n(lijst)                   bepaalt standaardafwijking voor steekproef
    mediaan(lijst)                    bepaalt de mediaan
    percentiel(lijst, percentage)     percentage getal tussen 0 en 100
    correlatie(lijst_a, lijst_b)      bepaalt correlatie matrix
    sorteer(lijst)                    sorteert een lijst van klein naar groot
    omdraaien(lijst)                  draai de volgorde van de lijst om
    alsdan(voorwaarde, als, dan)      bewerk lijst met voorwaarde per item
    is_nan(x)                         bepaalt of waarde een niet-getal is
    is_inf(x)                         bepaalt of waarde oneindig is
    gelijk(lijst_a, lijst_b)          per element kijken of waarden gelijk zijn
    groter(lijst_a, lijst_b)          per element kijken of waarde groter dan
    groter_gelijk(lijst_a, lijst_b)   idem, maar dan ook gelijk
    kleiner(lijst_a, lijst_b)         per element kijken of waarde kleiner dan
    kleiner_gelijk(lijst_a, lijst_b)  idem, maar dan ook gelijk
    alle(lijst)                       kijkt of alle elementen True zijn
    sommige(lijst)                    kijkt of er minimaal 1 element True is
    niet_alle(lijst)                  kijkt of er minimaal 1 element False is
    geen(lijst)                       kijkt of alle elementen False zijn
    of(a, b)                          kijkt of a of b True is
    en(a, b)                          kijkt of a en b True is
    niet(x)                           omdraaien van True naar False en andersom
    xof(a, b)                         True als a of b True is, en niet beide
    
WISKUNDIGE EIGENSCHAPPEN              (gebaseerd op Numpy module)
    nan                               float die geen getal is (not a number)
    inf                               oneindig groot
    pi                                3.141592653589793
    e                                 2.718281828459045

    """.strip())
    
    
###############################################################################

# eigenschappen

nan = np.nan
inf = np.inf
pi = np.pi
e = np.e

    
###############################################################################
    
# functies

_numpy_functions = dict(
    # fn of tuple(fn, check_type_eenheid, pre_verander_eenheid_fn, post_verander_eenheid_fn)
    sin = (np.sin, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    cos = (np.cos, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    tan = (np.tan, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    asin = (np.arcsin, '-', None, lambda eh, _: 'rad'),
    acos = (np.arccos, '-', None, lambda eh, _: 'rad'),
    atan = (np.arctan, '-', None, lambda eh, _: 'rad'),
    hypot = np.hypot, 
    graden = (np.degrees, '-', None, None),
    radialen = (np.radians, '-', None, None),
    sinh = (np.sinh, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    cosh = (np.cosh, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    tanh = (np.tanh, 'deg', lambda eh, _: 'rad', lambda eh, _: None),
    asinh = (np.arcsinh, '-', None, lambda eh, _: 'rad'),
    acosh = (np.arccosh, '-', None, lambda eh, _: 'rad'),
    atanh = (np.arctanh, '-', None, lambda eh, _: 'rad'),
    afronden = np.round,
    plafond = np.ceil,
    vloer = np.floor,
    plafond_0_vloer = np.fix,
    som = np.sum,
    product = np.prod,
    verschil = np.diff,
    optellen = np.add,
    aftrekken = np.subtract,
    vermenigvuldigen = (np.multiply, None, lambda eh, _: (  #### TODO #######################
        Waarde(1, (Waarde(1, eh)._eenheidbreuk)**2, config=None).eenheid)),
    delen = np.divide, ## None
    delen_aantal = np.floor_divide, ## None
    delen_rest = np.remainder,
    macht = (np.power, None, lambda eh, args: (
        Waarde(1, (Waarde(1, eh)._eenheidbreuk)**args[1], config=None).eenheid)),
    reciproke = np.reciprocal, ## reciproke fraction
    negatief = np.negative,
    # kruisproduct = np.cross,
    # inwendigproduct = np.dot,
    # exp = np.exp,
    # ln = np.log,
    # log = np.log10,
    # kgv = np.lcm,
    # ggd = np.gcd,
    # bijsnijden = np.clip,
    # wortel = np.sqrt,
    # wortel3 = np.cbrt,
    # teken = np.sign,
    # kopieer_teken = np.copysign,
    # is_positief = np.heaviside,
    # vervang_nan = np.nan_to_num,
    # verwijder_nan = lambda x: x[np.logical_not(np.isnan(x))],
    # interp = np.interp,
    # van_totmet_n = np.linspace,
    # van_tot_stap = np.arange,
    # gemiddelde = np.mean,
    # stdafw_pop = lambda x: np.std(x, ddof=0),
    # stdafw_n = lambda x: np.std(x, ddof=1),
    # mediaan = np.median,
    # percentiel = np.percentile,
    # correlatie = np.corrcoef,
    # sorteer = np.sort,
    # omdraaien = np.flip,
    # alsdan = np.where,
    # is_nan = np.isnan,
    # is_inf = np.isinf,
    # gelijk = np.equal,
    # groter = np.greater,
    # groter_gelijk = np.greater_equal,
    # kleiner = np.less,
    # kleiner_gelijk = np.less_equal,
    # alle = np.all,
    # sommige = np.any,
    # niet_alle = lambda x: ~np.all(x),
    # geen = lambda x: ~np.any(x),
    # of = np.logical_or,
    # en = np.logical_and,
    # niet = np.logical_not,
    # xof = np.logical_xor,
)
_numpy_functions['min'] = np.amin # reserverd keywords
_numpy_functions['max'] = np.amax
_numpy_functions['abs'] = np.fabs

def _wrap_functie(fn, check_type_eenheid=None, pre_verander_eenheid_fn=None, post_verander_eenheid_fn=None):
    def return_fn(*args, **kwargs):
        # pre
        eenheid = None
        waarde = False
        nieuwe_args = []
        for iarg, arg in enumerate(args):
            if isinstance(arg, Waarde):
                if (check_type_eenheid is not None
                        and arg.eenheid is not None
                        and arg._eenheidbreuk != Waarde(1)[check_type_eenheid]._eenheidbreuk):
                    raise ValueError('Eenheid \'{}\' in functie \'{}\' is niet geldig. '
                                     'Dit moet bijvoorbeeld \'{}\' zijn.'.format(
                                     arg.eenheid, fn.__name__, check_type_eenheid))
                waarde = True
                if pre_verander_eenheid_fn is not None:
                    eenheid = pre_verander_eenheid_fn(eenheid, args)
                    arg = arg.gebruik_eenheid(eenheid, check_type=False)
                else:
                    if iarg == 0:
                        eenheid = arg.eenheid
                    else:
                        arg = arg.eh(eenheid)
                nieuwe_args.append(float(arg))
            elif isinstance(arg, Lijst):
                arg_w = Waarde(1)[arg.eenheid]
                if (check_type_eenheid is not None
                        and arg.eenheid is not None
                        and arg_w._eenheidbreuk != Waarde(1)[check_type_eenheid]._eenheidbreuk):
                    raise ValueError('Eenheid \'{}\' in functie \'{}\' is niet geldig. '
                                     'Dit moet bijvoorbeeld \'{}\' zijn.'.format(
                                     arg_w.eenheid, fn.__name__, check_type_eenheid))
                eenheid = arg.eenheid if eenheid is None else eenheid
                if pre_verander_eenheid_fn is not None:
                    eenheid = pre_verander_eenheid_fn(eenheid, args)
                    arg = arg.gebruik_eenheid(eenheid, check_type=False)
                else:
                    if iarg == 0:
                        eenheid = arg.eenheid
                    else:
                        arg = arg.eh(eenheid)
                nieuwe_args.append(arg.array)
            else:
                nieuwe_args.append(arg)
            
        # call
        value = fn(*nieuwe_args, **kwargs)
        
        # post
        if post_verander_eenheid_fn is not None:
            eenheid = post_verander_eenheid_fn(eenheid, args)
        if isinstance(value, type(np.array([]))):
            l = Lijst(np.array(value, dtype='float64'))
            if eenheid is not None:
                if post_verander_eenheid_fn:
                    l = l.gebruik_eenheid(eenheid, check_type=False)
                else:
                    l = l.gebruik_eenheid(eenheid)
            return l
        elif waarde or eenheid:
            w = Waarde(value)
            if eenheid is not None:
                if post_verander_eenheid_fn:
                    w = w.gebruik_eenheid(eenheid, check_type=False)
                else:
                    w = w.gebruik_eenheid(eenheid)
            return w
        return value
    return return_fn

for fn_name, fn_arg in _numpy_functions.items():
    if callable(fn_arg):
        setattr(pyco, fn_name, _wrap_functie(fn_arg))
    elif len(fn_arg) == 2:
        setattr(pyco, fn_name, _wrap_functie(fn_arg[0], fn_arg[1]))
    elif len(fn_arg) == 3:
        setattr(pyco, fn_name, _wrap_functie(fn_arg[0], fn_arg[1], fn_arg[2]))
    elif len(fn_arg) == 4:
        setattr(pyco, fn_name, _wrap_functie(fn_arg[0], fn_arg[1], fn_arg[2], fn_arg[3]))

    
###############################################################################
    
