from pyco.interface import Document

doc = Document()
fn = doc.functies
x = doc.model.Waarde

@doc
class knikcontrole:

    N_Ed = x(120).kN   >>"""
    Rekenwaarde optredende normaalkracht
    """

    L = x(4).m   >>"""
    Lengte element
    """

    L_cr_factor = x(1.0)   >>"""
    Factor type oplegging:
    vast-los            -> 2.0
    scharnier-scharnier -> 1.0
    scharnier-vast      -> 0.7
    vast-vast           -> 0.5
    """

    A = x(2124).mm2   >>"""
    Oppervlakte profiel
    """

    b = x(100).mm   >>"""
    Breedte profiel
    """

    h = x(96).mm   >>"""
    Hoogte profiel
    """

    I_z = x(134e4).mm4   >>"""
    Traagheidsmoment zwakke as
    """

    t_f = x(8).mm   >>"""
    Dikte flens
    """

    E = x(210e3).MPa   >>"""
    Elasticiteitsmodulus
    """

    f_yk = x(235).MPa   >>"""
    Karakteristieke vloeigrens staal
    """

    gamma_m = x(1.0)   >>"""
    Materiaalfactor
    """

    I_z = x(fn.sqrt(I_z('mm4') / A('mm2'))).mm   >>"""
    Traagheidsstraal: sqrt(I_z / A)
    """

    L_cr = L * L_cr_factor   >>"""
    Kniklengte: L * L_cr_factor
    """

    lambda_abs = L_cr / I_z   >>"""
    Absolute slankheid: L_cr / I_z
    """

    lambda_1 = x(fn.pi * fn.sqrt(E('MPa') / f_yk('MPa')))   >>"""
    Invloed staalsterkte: pi * sqrt(E / E_yk)
    """

    lambda_rel = lambda_abs / lambda_1   >>"""
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
    kromme = x(kr)    >>"""
    Type knikkromme
    """

    knikdata = doc.data.KnikfactorStaal()
    chi = x(knikdata.interpoleer(
        input_kolom='lambda_rel',
        input_waarde=lambda_rel,
        output_kolom=kromme))   >>"""
    Knikcoëfficiënt
    """
    knikdata.plot(snijpunt=(lambda_rel, chi))

    N_Rd = x(chi * A * f_yk / gamma_m).kN._0   >>"""
    Opneembare normaalkracht: chi * A * F_yk / gamma_m
    """

    uc = N_Ed / N_Rd   >>"""
    Unity check knikcontrole: N_Ed / N_Rd
    """


@doc
class samenvatting:
    ucs = []

    uc_knik = knikcontrole.uc
    ucs.append(uc_knik())

    conclusie = x('voldoet' if all([uc <= 1.0 for uc in ucs]) else 'voldoet niet')   >>"""
    Alle unity checks moeten kleiner zijn dan 1.0
    """

doc.print_rapport()
