class Pyco:
    """
    Deze klasse wordt gebruikt als bibliotheek klasse voor de gebruiker.
    Deze is NIET bedoeld voor alle bestanden in de pyco map (kringverwijzing).
    
    from pyco import Pyco
    pc = Pyco()
    
    voorbeeld_waarde = pc.Waarde(3).mm
    """
    def __init__(self):
        import pyco.basis
        self.BasisObject = pyco.basis.BasisObject
        
        import pyco.waarde
        self.Waarde = pyco.waarde.Waarde
        
        import pyco.vector
        self.Vector = pyco.vector.Vector
        
        import pyco.knoop
        self.Knoop = pyco.knoop.Knoop
        
        import pyco.lijn
        self.Lijn = pyco.lijn.Lijn
        
        import pyco.vorm
        self.Vorm = pyco.vorm.Vorm
        
        if True:
            import pyco.rechthoek
            self.Rechthoek = pyco.rechthoek.Rechthoek

            import pyco.cirkel
            self.Cirkel = pyco.cirkel.Cirkel
            
        import pyco.materiaal
        self.Materiaal = pyco.materiaal.Materiaal