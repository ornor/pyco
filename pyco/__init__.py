# afhankelijke externe bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#-------------------------------------

import pyco.basis
BasisObject = pyco.basis.BasisObject

import pyco.waarde
Waarde = pyco.waarde.Waarde
W = pyco.waarde.Waarde

import pyco.lijst
Lijst = pyco.lijst.Lijst
L = pyco.lijst.Lijst

from pyco.functions import import_all
for k, v in import_all.items():
    setattr(pyco, k, v)

import pyco.data
Data = pyco.data.Data

import pyco.knoop
Knoop = pyco.knoop.Knoop

import pyco.lijn
Lijn = pyco.lijn.Lijn

import pyco.vorm
Vorm = pyco.vorm.Vorm

import pyco.rechthoek
Rechthoek = pyco.rechthoek.Rechthoek

import pyco.cirkel
Cirkel = pyco.cirkel.Cirkel
    
import pyco.venster
TekstVenster = pyco.venster.TekstVenster
FiguurVenster = pyco.venster.FiguurVenster
BestandsnaamVenster = pyco.venster.BestandsnaamVenster

import pyco.figuur
Figuur = pyco.figuur.Figuur

import pyco.materiaal
Materiaal = pyco.materiaal.Materiaal

import pyco.document
Document = pyco.document.Document

import pyco.macro
Macro = pyco.macro.Macro

class macro:
    import pyco.macros.ligger_op_twee_steunpunten
    Ligger_op_twee_steunpunten = pyco.macros.ligger_op_twee_steunpunten.Ligger_op_twee_steunpunten