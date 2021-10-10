from pyco.interface import Document

doc = Document()
fn = doc.functies
x = doc.model.Waarde

@doc
class knikcontrole:

    N_Ed = x(120).kN >> """
    Rekenwaarde optredende normaalkracht
    """

    L = x(4).m >> """
    Lengte element
    """

    L_cr_factor = x(1.0) >> """
    Factor type oplegging:
    vast-los            -> 2.0
    scharnier-scharnier -> 1.0
    scharnier-vast      -> 0.7
    vast-vast           -> 0.5
    """

    A = x(2124).mm2 >> """
    Oppervlakte profiel
    """

    b = x(100).mm >> """
    Breedte profiel
    """

    h = x(96).mm >> """
    Hoogte profiel
    """

    I_z = x(134e4).mm4 >> """
    Traagheidsmoment zwakke as
    """

    t_f = x(8).mm >> """
    Dikte flens
    """

    E = x(210e3).MPa >> """
    Elasticiteitsmodulus
    """

    f_yk = x(235).MPa >> """
    Karakteristieke vloeigrens staal
    """

    gamma_m = x(1.0) >> """
    Materiaalfactor
    """

    I_z = x(fn.sqrt(I_z('mm4') / A('mm2'))).mm >> """
    Traagheidsstraal: sqrt(I_z / A)
    """

    L_cr = L * L_cr_factor >> """
    Kniklengte: L * L_cr_factor
    """

    lambda_abs = L_cr / I_z >> """
    Absolute slankheid: L_cr / I_z
    """

    lambda_1 = x(fn.pi * fn.sqrt(E('MPa') / f_yk('MPa'))) >> """
    Invloed staalsterkte: pi * sqrt(E / E_yk)
    """

    lambda_rel = lambda_abs / lambda_1 >> """
    Relatieve slankheid: lambda_abs / lambda_1
    """

    if h('mm')/b('mm') > 1.2:
        if t_f('mm') <= 40:
            kr = 'b' if f_yk('MPa') < 420 else 'a0'
        else:
            kr = 'c' if f_yk('MPa') < 420 else 'a'
    else:
        if t_f('mm') <= 100:
            kr = 'c' if f_yk('MPa') < 420 else 'a'
        else:
            kr = 'd' if f_yk('MPa') < 420 else 'c'
    kromme = x(kr) >> """
    Type knikkromme
    """

    knikdata = doc.data.KnikfactorStaal()
    #knikdata.plot()
    chi = x(knikdata.interpoleer('lambda_rel', lambda_rel, kromme)) >> """
    Knikcoëfficiënt
    """

    N_Rd = x(chi * A * f_yk / gamma_m).kN._0 >> """
    Opneembare normaalkracht: chi * A * F_yk / gamma_m
    """

    uc = N_Ed / N_Rd >> """
    Unity check knikcontrole: N_Ed / N_Rd
    """


@doc
class samenvatting:
    uc_knik = knikcontrole.uc

twee_punten = {
    'punt 1: $\\theta_\\pi$': (4, 2),
    'punt 2: $\\omega_3$': (-1, 6.5),
}

doc.model.Figuur(
        breedte=7,
        hoogte=7,
        raster=True,
        legenda=True,
        titel='Kunst',
        x_as_titel='variabele $\\pi$',
        y_as_titel='verticale as',
        gelijke_assen=True,
        verberg_assen=False,
        x_as_log=False,
        y_as_log=False,
    ).lijn(
        coordinaten=((2, 0), (3, 7), (-2, 4), (2, 0)),
        breedte=3,
        kleur='red',
        vullen=False,
        arcering='/',
        naam='rood vlak',
    ).lijn(
        coordinaten=((-1, 0), (0, 6)),
        breedte=3,
        kleur='blue',
        naam='rechte $\\alpha$-lijn',
    ).punt(
        coordinaten=list(twee_punten.values()),
        breedte=10,
        kleur='gold',
        stijl='>',
        naam='twee punten',
    ).tekst(
        coordinaten=list(twee_punten.values()),
        teksten=list(twee_punten.keys()),
        kleur='brown',
        tekst_grootte='large', # {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        tekst_font='sans-serif', # {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'}
        tekst_stijl='normal', # {'normal', 'italic', 'oblique'}
        tekst_gewicht='bold', # {'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'}
        hor_uitlijnen='center', # {'center', 'right', 'left'}
        vert_uitlijnen='center', # {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
        roteren=30,
    ).kolom(
        coordinaten=((3, 8), (6, 4), (8, 1)),
        kleur='pink',
        breedte=0.4,
        lijn_kleur='peru',
        lijn_breedte=2,
        naam='bar plot',
    ).fx(
        functie = lambda x: x**2 + 3*fn.sin(x),
        x = (-2, 3),
        breedte = 2,
        kleur = 'green',
        naam = 'sinus parabool',
    )()

doc.model.Figuur(
        raster=True,
    ).fx(
        functie = lambda x: 0.1*x**2 + 5*fn.sin(x) + 2,
        x = (-5, 10),
    )()

doc.print_rapport()
