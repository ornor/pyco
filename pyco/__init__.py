# afhankelijke externe bibliotheken
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#-------------------------------------

import pyco.basis
BasisObject = pyco.basis.BasisObject
BiebItem = pyco.basis.BiebItem

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

#-------------------------------------
 
def import_bieb(pad=None, verbose=False):
    import os.path, glob, importlib, inspect
    
    BIEB_MODULES_MAP = 'bieb_modules'
    pad = os.path.join(os.path.dirname(__file__), BIEB_MODULES_MAP) if pad is None else pad
    
    if not os.path.isdir(pad):
        raise ValueError('opgegeven pad is geen geldige mapnaam: {}'. format(pad))
        
    if verbose:
        print('Importeer bieb modules uit de map: {}'.format(pad))
        
    if hasattr(pyco, 'bieb'):
        bieb_container = getattr(pyco, 'bieb')
    else:
        class bieb_container: pass
        
    if hasattr(pyco, 'bieb') and hasattr(pyco.bieb, 'macro'):
        macro_container = getattr(pyco.bieb, 'macro')
    else:
        class macro_container: pass
    
    if hasattr(pyco, 'bieb') and hasattr(pyco.bieb, 'data'):
        data_container = getattr(pyco.bieb, 'data')
    else:
        class data_container: pass
    
    if hasattr(pyco, 'bieb') and hasattr(pyco.bieb, 'figuur'):
        figuur_container = getattr(pyco.bieb, 'figuur')
    else:
        class figuur_container: pass
    
    if hasattr(pyco, 'bieb') and hasattr(pyco.bieb, 'document'):
        document_container = getattr(pyco.bieb, 'document')
    else:
        class document_container: pass

    for module_naam in [os.path.basename(f)[:-3] for f in glob.glob(
                os.path.join(pad, '*.py')
            ) if os.path.isfile(f) and not f.endswith('__init__.py')]:
        module_obj = importlib.import_module('pyco.{}.'.format(BIEB_MODULES_MAP) + module_naam)
        bieb_klasses = [o for o in dir(module_obj) if not o.startswith('_')]
        for bieb_klasse in bieb_klasses:
            bieb_klasse_obj = getattr(module_obj, bieb_klasse)
            if verbose:
                print('Importeer: {}'.format(bieb_klasse))
            if inspect.isclass(bieb_klasse_obj) and issubclass(bieb_klasse_obj, BiebItem):
                if issubclass(bieb_klasse_obj, Macro):
                    setattr(macro_container, bieb_klasse, bieb_klasse_obj)
                elif issubclass(bieb_klasse_obj, Data):
                    setattr(data_container, bieb_klasse, bieb_klasse_obj)
                elif issubclass(bieb_klasse_obj, Figuur):
                    setattr(figuur_container, bieb_klasse, bieb_klasse_obj)
                elif issubclass(bieb_klasse_obj, Document):
                    setattr(document_container, bieb_klasse, bieb_klasse_obj)
                else:
                    setattr(bieb_container, bieb_klasse, bieb_klasse_obj)
    
    setattr(pyco, 'bieb', bieb_container)      
    setattr(pyco.bieb, 'macro', macro_container)
    setattr(pyco.bieb, 'data', data_container)
    setattr(pyco.bieb, 'figuur', figuur_container)
    setattr(pyco.bieb, 'document', document_container)
        
import_bieb()