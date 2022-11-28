import pandas as pd
import numpy as np

import pyco.waarde
import pyco.lijst

class pc:
    BasisObject = pyco.basis.BasisObject
    Waarde = pyco.waarde.Waarde
    Lijst = pyco.lijst.Lijst

class Register(pc.BasisObject):
    """
    Een Pandas DataFrame waarbij kolommen een eenheid kunnen hebben.

    AANMAKEN REGISTER    
        t = Register({'kolom1': 'eenheid1', 'kolom2': 'eenheid2'})   # '-', '' of None

 
    """

    def __init__(self, lijst_dict):
        super().__init__()
        
        if not isinstance(lijst_dict, dict):
            raise TypeError("type argument 1 is GEEN dict: {}".format(type(lijst_dict)))

        self.eigenschappen = list(lijst_dict.keys())
        self.eenheden = list(lijst_dict.values())
        self._kolomindex = pd.MultiIndex.from_tuples([(gh, eh) for gh, eh in lijst_dict.items()])
        self._dataframe = pd.DataFrame([], columns=self._kolomindex)
        
        
    def toevoegen(self, *args):
        """
        r1.toevoegen([7,5,3,1])
        r1.toevoegen(4,5,6,7)
        r1.toevoegen(pc.Lijst(4,9,6,70))
        r1.toevoegen((14,15,16,17))
        """
        if len(args) == 1:
            if isinstance(args[0], list) or isinstance(args[0], tuple):
                args = args[0]
            elif isinstance(args[0], pc.Lijst):
                args = args[0].array
            else:
                args = [args[0]]
                
        if len(args) != len(self.eigenschappen):
            raise ValueError('aantal waardes ({}) is niet gelijk aan aantal kolomnamen ({}: {})'.format(len(args), len(self.eigenschappen), ', '.join(["'{}'".format(e) for e in self.eigenschappen])))
    
        tmp_df = pd.DataFrame([args], columns=self._kolomindex)
        self._dataframe = pd.concat([self._dataframe, tmp_df], ignore_index=True)
        
        
    @property    
    def df(self):
        return self._dataframe
    
    
    def __getitem__(self, eigenschap_bereik):
        """
        Retourneert een eigenschap als Lijst (tekst invoer) of een aantal rijen van DataFrame (getal/bereik invoer).
        
        register_obj['eigenschap(kolom)naam']
        register_obj[0]     # Python list met waardes van 1e invoer (rij)
        register_obj[3:8]   # Python list met waardes (ook Python list) van 4e t/m 8e invoer (rijen)
        register_obj[::2]   # Python list met alle oneven rijnummers
        """
        if isinstance(eigenschap_bereik, str):
            eigenschap = eigenschap_bereik
            if eigenschap not in self.eigenschappen:
                raise ValueError("eigenschap '{}' niet aanwezig in de beschikbare eigenschappen: "
                                 "{}".format(eigenschap, ', '.join(["'{}'".format(e) for e in self.eigenschappen])))

            eenheid = self.eenheden[self.eigenschappen.index(eigenschap)]
            return pc.Lijst(self.df[eigenschap][eenheid].values.tolist()).gebruik_eenheid(eenheid)
        else:
            bereik = eigenschap_bereik
            rijen_lijst = self.df.iloc[bereik].values.tolist()
            return rijen_lijst
    
    def __repr__(self):
        object_str = self.__str__()
        return 'pyco.Register object:\n' + len(object_str.split('\n')[0])*'-' + '\n' + object_str
    
    def __str__(self):
        return str(self.df)


