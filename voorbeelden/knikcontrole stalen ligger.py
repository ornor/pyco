from pyco.interface import Document

doc = Document()
fn = doc.functies
x = doc.model.Waarde

doc.titel = 'Knikcontrole stalen ligger'

doc('Voorbeeld uit de cursus Constructie 2')


@doc
class knikcontrole:

    N_Ed = x(100).kN   >>\
    "Rekenwaarde optredende normaalkracht"

    L = x(4).m   >>\
    "Lengte element"

    L_cr_factor = x(1.0)   >>\
    """
    Factor type oplegging:
    vast-los            -> 2.0
    scharnier-scharnier -> 1.0
    scharnier-vast      -> 0.7
    vast-vast           -> 0.5
    """

    A = x(2124).mm2   >>\
    "Oppervlakte profiel"

    b = x(100).mm   >>\
    "Breedte profiel"

    h = x(96).mm   >>\
    "Hoogte profiel"

    I_z = x(134e4).mm4   >>\
    "Traagheidsmoment zwakke as"

    t_f = x(8).mm   >>\
    "Dikte flens"

    E = x(210e3).MPa   >>\
    "Elasticiteitsmodulus"

    f_yk = x(235).MPa   >>\
    "Karakteristieke vloeigrens staal"

    gamma_m = x(1.0)   >>\
    "Materiaalfactor"

    i_z = x(fn.wortel(float(I_z.mm4) / float(A.mm2))).mm   >>\
    "Traagheidsstraal: sqrt(I_z / A)"

    L_cr = L * L_cr_factor   >>\
    "Kniklengte: L * L_cr_factor"

    lambda_abs = L_cr / i_z   >>\
    "Absolute slankheid: L_cr / i_z"

    lambda_1 = x(fn.pi * fn.wortel(float(E.MPa) / float(f_yk.MPa)))   >>\
    "Invloed staalsterkte: pi * sqrt(E / E_yk)"

    lambda_rel = lambda_abs / lambda_1   >>\
    "Relatieve slankheid: lambda_abs / lambda_1"

    if float(h.mm)/float(b.mm) > 1.2:
        if float(t_f.mm) <= 40:
            kr = 'b' if float(f_yk.MPa) < 420 else 'a0'
        else:
            kr = 'c' if float(f_yk.MPa) < 420 else 'a'
    else:
        if float(t_f.mm) <= 100:
            kr = 'c' if float(f_yk.MPa) < 420 else 'a'
        else:
            kr = 'd' if float(f_yk.MPa) < 420 else 'c'
    kromme = x(kr)    >>\
    "Type knikkromme"

    knikdata = doc.data.KnikfactorStaal()
    chi = x(knikdata.interpoleer(
        input_kolom='lambda_rel',
        input_waarde=lambda_rel,
        output_kolom=kromme))   >>\
    "Knikcoëfficiënt"
    chi_fig = knikdata.figuur(snijpunt=(lambda_rel, chi))

    N_Rd = x(chi * A * f_yk / gamma_m).kN._0   >>\
    "Opneembare normaalkracht: chi * A * F_yk / gamma_m"

    uc = N_Ed / N_Rd   >>\
    "Unity check knikcontrole: N_Ed / N_Rd"


@doc
class samenvatting:
    ucs = []

    uc_knik = knikcontrole.uc
    ucs.append(float(uc_knik))

    conclusie = x('voldoet' if all([uc <= 1.0 for uc in ucs]) else 'voldoet niet')   >>\
    "Alle unity checks moeten kleiner zijn dan 1.0"


doc.print_console()

#doc.print_html()
