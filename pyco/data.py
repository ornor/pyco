import pandas as pd
import numpy as np
from collections import namedtuple

import pyco.basis
import pyco.waarde
import pyco.lijst

class pc:
    BasisObject = pyco.basis.BasisObject
    Waarde = pyco.waarde.Waarde
    Lijst = pyco.lijst.Lijst

class Data(pc.BasisObject):
    """
    Een Pandas DataFrame waarbij eigenschappen een eenheid kunnen hebben.
    Eigenschap moet een geldige Python naam opmaak hebben en mag niet 'data' zijn.

    AANMAKEN DATA  
        d = Data(eigenschap1='eenheid1',           als eenheid dimensieloos:
                 eigenschap2='eenheid2')             dan gebruik '-', '' of None
        d = Data(eigenschap1='eh1', data=...)      direct toevoegen van data
                  
    DATA EIGENSCHAPPEN
        d.eigenschappen           lijst met aanwezige kolomnamen
        d.eenheden                lijst met eenheden die bij kolommen horen
        d.df                      Pandas DataFrame object 
        d.DataRij                 klasse die een rij met eigenschappen beschrijft
    
    DATARIJ
        dr1 = d.DataRij(eigenschap1=waarde1, eigenschap2=waarde2)
        dr2.waardes                   retourneert attributen met Waarde objecten
        
    TOEVOEGEN DATA REGEL    in onderstaande gevallen: 4 eigenschappen (kolommen)
        d.toevoegen(d.DataRij( ... ))      een DataRij object
        d.toevoegen([7,5,3,1])             een Python list object
        d.toevoegen(4,5,6,7)               losse argumenten
        d.toevoegen(pc.Lijst(4,9,6,70))    een Lijst object
        d.toevoegen((14,15,16,17))         een Python tuple object
        d.toevoegen(1,2)                   2 laatste kolommen worden met
                                                   standaard waarde ingevuld (0)
        d.toevoegen(1,2,standaard=pc.nan)  andere standaard waarde
        d.toeveogen([(1,2,3,4), (3,4,5,6), (5,6,7,8)])  of 2D Python lijst/tuple

    OPHALEN DATA EIGENSCHAP       
        d['eigenschap1']          een Lijst object (kolom uit dataframe)
        d.eigenschap1             ook beschikbaar als attribuut van object
        d[0]                      DataRij object van 1e invoer
        d[3:8]                    Python list met waardes (in Datarij)
                                                            van 4e t/m 8e invoer
        d[::2]                    Python list met alle oneven rijnummers
        d[:, 1:3]                 Python list met 2e en 3e kolom
                                                  (alleen waarden, geen eenheid) 
                                                  
        d[0].eigenschap1          is alleen getal (of tekst) zelf (van 1e rij)
        d[0].waardes.eigenschap1  is pc.Waarde object dat dit getal bevat
                                                  
    ZOEKEN EN INTERPOLEREN IN INDEX KOLOM        1e kolom wordt als index gezien
        d.zoek('waarde 1e kolom') geeft een DataRij object horende bij waarde
        d.zoek(exact_getal)       geeft een DataRij object horende bij waarde                      
        d.zoek(getal)             interpoleert getal in 1e kolom en geeft DataRij
        d.zoek(waarde, eigenschap='es3')  gebruik andere kolom als index kolom

    """

    def __init__(self, **lijst_dict):
        super().__init__()
        
        toevoegen_data = None
        if 'data' in lijst_dict:
            toevoegen_data = lijst_dict['data']
            del lijst_dict['data']
            
        toevoegen_bronnen = None
        if 'bronnen' in lijst_dict:
            toevoegen_bronnen = lijst_dict['bronnen']
            del lijst_dict['bronnen']
            
        lijst_dict = {k:(v if isinstance(v, str) and len(v) > 0 else '-') for k, v in lijst_dict.items()}
        self._dataframe = pd.DataFrame([], columns=pd.MultiIndex.from_tuples(
                [(gh, eh) for gh, eh in lijst_dict.items()]))
        
        if toevoegen_data is not None:
            self.toevoegen(toevoegen_data)
            
        self._bronnen = []
        if toevoegen_bronnen is not None:
            if isinstance(toevoegen_bronnen, str):
                toevoegen_bronnen = [toevoegen_bronnen]
            self._bronnen = [b for b in toevoegen_bronnen]
        
    @property
    def eigenschappen(self):
        """Lijst met aanwezige kolomnamen."""
        return [es for es, _ in self.df.columns]
    
    @property
    def eenheden(self):
        """Lijst met eenheden die bij eigenschappen (kolommen) horen."""
        return [eh for _, eh in self.df.columns]
    
    @property
    def bronnen(self):
        """Lijst met bronvermeldingen."""
        return self._bronnen
    
    @property
    def DataRij(self):
        """Retourneert een namedtuple klasse met kolomnamen."""
        eigenschappen = self.eigenschappen
        eenheden = self.eenheden
        cls = namedtuple('DataRij', eigenschappen)
        
        @property
        def waardes(cls_self):
            """Methode van DataRij attributen met Waarde objecten retourneert."""
            class waarde_klasse: pass
        
            for es, w in cls_self._asdict().items():
                setattr(waarde_klasse, es, pc.Waarde(w).eh(
                                              eenheden[eigenschappen.index(es)]))
            return waarde_klasse
        
        cls.waardes = waardes
        
        return cls

    def toevoegen(self, *args, standaard=0, **kwargs):
        """Een nieuwe rij toevoegen"""
        eigenschappen = self.eigenschappen
        eenheden = self.eenheden
        if len(kwargs) > 0:
            args = [kwargs.get(es, standaard) for es in eigenschappen]
                
        if len(args) == 1:
            if isinstance(args[0], self.DataRij):
                args = list(args[0])
            if isinstance(args[0], list) or isinstance(args[0], tuple):
                if all([(
                            (isinstance(a, list) or isinstance(a, tuple))
                            and len(a) == len(eigenschappen)
                        ) for a in args[0]]):
                    for subargs in args[0]:
                        self.toevoegen(subargs)
                    return
                else:
                    args = args[0]
            elif isinstance(args[0], pc.Lijst):
                args = args[0].array
            else:
                args = [args[0]]
                
        if len(args) > len(eigenschappen):
            args = args[:len(eigenschappen)]
        elif len(args) < len(eigenschappen):
            args = list(args) + [standaard]*(len(eigenschappen) - len(args))
        
        tmp_df = pd.DataFrame([args], columns=pd.MultiIndex.from_tuples(
                [(es, eh) for es, eh in zip(eigenschappen, eenheden)]))
        self._dataframe = pd.concat([self._dataframe, tmp_df], ignore_index=True)
        
    def toevoegen_bronnen(self, bronnen, *overige_bronnen):
        if isinstance(bronnen, str):
            bronnen = [bronnen]
        if len(overige_bronnen) > 0:
            bronnen += overige_bronnen
        self._bronnen += list(bronnen)
        
    @property    
    def df(self):
        """Een Pandas DataFrame object retourneren."""
        return self._dataframe
    
    def coordinaten(self, eigenschap1, eigenschap2):
        """Retourneert een tuple met tuples (eigenschap1, eigenschap2)"""
        return tuple(zip(self[eigenschap1].array, self[eigenschap2].array))
    
    
    def zoek(self, waarde, eigenschap=None):
        """Zoek waarde in index kolom, en geef corresponderende RijData.
        Als getal dan interpoleer waardes. Standaard index is 1e kolom."""
        i_index = 0
        eigenschappen = self.eigenschappen
        if eigenschap is not None:
            if eigenschap not in eigenschappen:
                raise ValueError('Eigenschap is niet geldig: {}'.format(eigenschap))
            i_index = eigenschappen.index(eigenschap)
            
        if isinstance(waarde, str):
            kolom_1 = self.__getitem__(eigenschappen[i_index]).array.tolist()
            if not waarde in kolom_1:
                return None
            idx = kolom_1.index(waarde)
            return self.__getitem__(idx)
        elif isinstance(waarde, int) or isinstance(waarde, float):
            kolom_1 = self.__getitem__(eigenschappen[i_index]).array.tolist()
            if len(kolom_1) < 1:
                return None
            if waarde in kolom_1:
                idx = kolom_1.index(waarde)
                return self.__getitem__(idx)
            # interpoleer waardes
            def zijn_getallen(a, b):
                return ((isinstance(a, float) or isinstance(a, int))
                            and (isinstance(b, float) or isinstance(b, int)))
            berekende_lijst = []
            for i_rij in range(1, len(kolom_1)):
                vorige_waardes = self.df.iloc[i_rij-1].values.tolist()
                deze_waardes = self.df.iloc[i_rij].values.tolist()
                vorige_index = vorige_waardes[i_index]
                deze_index = deze_waardes[i_index]
                if (zijn_getallen(vorige_index, deze_index)
                        and ((waarde > vorige_index and waarde < deze_index)
                            or (waarde < vorige_index and waarde > deze_index))
                        and (deze_index - vorige_index) != 0
                        and (waarde - vorige_index) != 0):
                    for a, b in zip(vorige_waardes, deze_waardes):
                        if zijn_getallen(a, b):
                            berekende_lijst.append(a + 
                                ((waarde - vorige_index) / (deze_index - vorige_index))
                                * (b - a))
                        else:
                            berekende_lijst.append(np.nan)
                    return self.DataRij(*berekende_lijst)
        else:
            return None
    
    def __getitem__(self, eigenschap_bereik):
        """Retourneert een eigenschap als Lijst (tekst invoer) of een aantal rijen van DataFrame (getal/bereik invoer)."""
        eigenschappen = self.eigenschappen
        eenheden = self.eenheden
        if isinstance(eigenschap_bereik, str):
            eigenschap = eigenschap_bereik
            if not eigenschap in eigenschappen:
                raise ValueError('Eigenschap \'{}\' is geen geldige eigenschap ({}).'.format(
                        eigenschap,
                        ', '.join(eigenschappen)))
            eenheid = eenheden[eigenschappen.index(eigenschap)]
            return pc.Lijst(self.df[eigenschap][eenheid].values.tolist()).gebruik_eenheid(eenheid)
        else:
            bereik = eigenschap_bereik
            rijen_lijst = self.df.iloc[bereik].values.tolist()
            if len(rijen_lijst) == 0:
                return []
            elif not isinstance(rijen_lijst[0], list) and len(rijen_lijst) == len(eigenschappen):
                return self.DataRij(*rijen_lijst)
            elif isinstance(rijen_lijst[0], list) and len(rijen_lijst[0]) == len(eigenschappen):
                return [self.DataRij(*rij) for rij in rijen_lijst]
            return rijen_lijst
        
    def __getattr__(self, name):
        """Retourneert een eigenschap (zie __getitem__) ook als attribuut van object."""
        if name in self.eigenschappen:
            return self.__getitem__(name)
    
    def __repr__(self):
        object_str = self.__str__()
        lijn = len(object_str.split('\n')[0])*'-'
        bronnen = ''
        if len(self.bronnen) == 1:
            bronnen = self.bronnen[0]
        elif len(self.bronnen) > 1:
            bronnen = '\n'.join(['* {}'.format(b) for b in self.bronnen])
        return ('pyco.Data object:\n' 
                    + lijn + '\n' 
                    + object_str + '\n' 
                    + lijn + '\n' 
                    + bronnen)
    
    def __str__(self):
        return str(self.df)


