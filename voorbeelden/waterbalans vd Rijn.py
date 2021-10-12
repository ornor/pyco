from pyco.interface import Document

doc = Document()
x = doc.model.Waarde

doc('Voorbeeld uit de cursus Water 1')

@doc
class opgave:

    A = x(16e4).km2   >>\
    "Oppervlakte stroomgebied"

    P = x(910, 'mm/j')   >>\
    "Gemiddelde jaarneerslag"

    R_u = x(2200, 'm3/s')   >>\
    "Gemiddelde oppervlakteafvoer"

    O = x(16.8e9, 'm3/j')   >>\
    "Gemiddelde waterontrekking industrie, drinkwater e.d."

    O_i = x(16.0e9, 'm3/j')   >>\
    "Gemiddelde waterlozing industrie, afvalwater e.d."

    Sigma_Delta_V = x(0, 'm3/s')   >>\
    "Berginsverandering"

    G_i = x(0, 'm3/s')   >>\
    "Ondergrondse instroom"

    G_u = x(0, 'm3/s')   >>\
    "Ondergrondse uitstroom"

doc('Stel de waterbalans voor de Rijn op en bereken de ontbrekende term, uitgedruk in mm/j.')

@doc
class uitwerking:

    P = x(opgave.P)

    R_i = x(0, 'mm/j')   >>\
    "We bekijken immers het hele stroomgebied"

    G_i = opgave.G_i / opgave.A

    O_i = opgave.O_i / opgave.A

    R_u = opgave.R_u / opgave.A

    G_u = opgave.G_u / opgave.A

    O_u = opgave.O / opgave.A

    Sigma_Delta_V = opgave.Sigma_Delta_V / opgave.A

    E = (P + R_i + O_i + G_i - R_u - G_u - O_u - Sigma_Delta_V)['mm/j']._0   >>\
    " P + R_i + O_i + G_i - R_u - G_u - O_u - Sigma_Delta_V"


doc.print_rapport()
