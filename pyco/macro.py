from abc import ABC, abstractmethod

import pyco.basis

class pc:
    BasisObject = pyco.basis.BasisObject
    

class Macro(pc.BasisObject, ABC):
    """
    Macro klasse.
    
    
    class VoorbeeldMacro(pc.Macro):
        "Hier komt helptekst"
        
        def __init__(self, config1=None, config2=None):
            self.document = pc.Document('Een titel')
            self.config1 = config1 if config1 is None else config1
            self.config2 = config2 if config2 is None else config2
            
        def extra_methode_om_data_in_te_voeren(self, param1, param2):
            self.param1 = param1 + param2
            return self   # altijd instantie retourneren
            
        def __call__(self):
            doc = self.document
            
            @doc
            class eerste_deel:
                a = ...
                b = ...
                
            self.eerste_deel = eerste_deel
            
            @doc
            class tweede_deel:
                c = ...
                d = ...
                
            self.tweede_deel = tweede_deel
            
            return self   # altijd instantie retourneren
            
    
    Macro kan nu gebruikt worden:
    
        voorbeeld = VoorbeeldMacro(
                        config1=..., config2=...
                    ).extra_methode_om_data_in_te_voeren(
                        param1=..., param2=...
                    )()
                    
        voorbeeld.eerste_deel.a   # retourneert waarde
        voorbeeld.tweede_deel.c   # retourneert waarde
        voorbeeld.document()      # weergeven document 
        voorbeeld.print_help()    # print helptekst van VoorbeeldMacro
    
    """
    
    def __init__(self):
        super().__init__()
        
    @abstractmethod
    def __call__(self):
        pass