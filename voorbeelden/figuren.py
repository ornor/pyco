from pyco.model import Figuur

twee_punten = {
    'punt 1: $\\theta_\\pi$': (4, 2),
    'punt 2: $\\omega_3$': (-1, 6.5),
}

Figuur(
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
        x = (-4, 10),
    )()
