# pyco handleiding

Begin alle documenten met onderstaande import.


```python
import pyco as pc
```

De pyco bibliotheek is afhankelijk van drie externe bibliotheken:

* numpy (https://numpy.org) beschikbaar via `pc.np`
* pandas (https://pandas.pydata.org/) beschikbaar via `pc.pd`
* matplotlib (https://matplotlib.org/) pyplot module beschikbaar via `pc.plt`

## Inhoud
Alle pyco klasses beginnen met een hoofdletter. Alle functies en eigenschappen beginnen met een kleine letter.

* [Waarde](#Waarde)
* [Lijst](#Lijst)
* [Data](#Data)
* [Knoop](#Knoop)
* [Lijn](#Lijn)
* [Vorm](#Vorm)
    - [Rechthoek](#Rechthoek)
    - [Cirkel](#Cirkel)
* [Figuur](#Figuur)
* [Materiaal](#Materiaal)
* [pyco functies en eigenschappen](#Functies)

## Waarde

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Waarde.print_help()
```

    
    +----------+
    |  Waarde  |
    +----------+
    
    Bevat een getal en bijhorende eenheid.
    
    AANMAKEN WAARDE
        w = Waarde(getal)
        w = Waarde(getal, eenheid_tekst)
        w2 = w.kopie()          maak een kopie (nieuw object) met zelfde eigenschappen    
    
    AANPASSEN EENHEID           omzetten van eenheid naar andere eenheid
        w.eenheid               huidige eenheid opvragen (tekst of None)
        w.eenheid = 'N/mm2'     eenheid aanpassen
        w = w['N/mm2']          eenheid aanpassen, retourneert object
        w.gebruik_eenheid('mm') eenheid aanpassen, retourneert object
        w.eh('mm')              eenheid aanpassen, retourneert object
        w = w.N_mm2             kan voor een aantal standaard gevallen (zie lijst onderaan)
    
    AANPASSEN AFRONDING         pas afgerond wanneer waarde wordt getoond als tekst
        w = w[0]                kan voor alle gehele getallen
        w = w._0                kan voor 0 t/m 9 (cijfers achter de komma)
    
    OMZETTEN WAARDE NAAR TEKST  resulteert in nieuw string object
                                    -> gebruikt afronding indien opgegeven
        tekst = str(w)          of automatisch met bijvoorbeeld print(w)
        tekst = format(w,'.2f') format configuratie meegeven voor getal
              = w.format('.2f')
    
    OMZETTEN WAARDE NAAR GETAL  resulteert in nieuw float object
        getal = float(w)        omzetten met standaard eenheid
        getal = float(w['eh'])  eerst eenheid definiëren voor omzetten waarde
    
    MOGELIJKE BEWERKINGEN       resulteert in nieuw Waarde object
        w3 = w1 + w2            waarde optellen bij waarde
        w3 = w1 - w2            waarde aftrekken van waarde
        w3 = w1 * w2            waarde vermenigvuldigen met waarde
        w3 = w1 / w2            waarde delen door waarde
        w2 = n * w1             getal vermenigvuldigen met waarde
        w2 = w1 * n             waarde vermenigvuldigen met getal
        w2 = n / w1             getal delen door waarde
        w2 = w1 / n             waarde delen door getal
        w2 = w1 ** n            waarde tot de macht een geheel getal
        w2 = abs(w1)            maakt waarde altijd positief
        w2 = +w1                behoud teken
        w2 = -w1                verander teken (positief vs. negatief)
    
    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        w1 == w2                is gelijk aan
        w1 == getal             de float() van waarde is gelijk aan getal
        w1 != w2                is niet gelijk aan
        w1 >  w2                is groter dan
        w1 <  w2                is kleiner dan
        w1 >= w2                is groter dan of gelijk aan
        w1 <= w2                is kleiner dan of gelijk aan
        w1 &  w2                eenheden zijn zelfde type
        
    WISKUNDIGE FUNCTIES         
        w.sin()                 sinus (alleen getallen en hoeken)
        w.cos()                 cosinus (alleen getallen en hoeken)
        w.tan()                 tangens (alleen getallen en hoeken)
        w.asin()                arcsinus (omgekeerde sin, alleen getallen)
        w.acos()                arccosinus (omgekeerde cos, alleen getallen)
        w.atan()                arctangens (omgekeerde tan, alleen getallen)
        w.sinh()                hyperbolische sinus (getallen en hoeken)
        w.cosh()                hyperbolische cosinus (getallen en hoeken)
        w.tanh()                hyperbolische tangens (getallen en hoeken)
        w.asinh()               arcsinus hyperb. (omgekeerde asinh, getallen)
        w.acosh()               arccosinus hyperb. (omgekeerde acosh, getallen)
        w.atanh()               arctangens hyperb. (omgekeerde atanh, getallen)
        w.afronden(n)           rond af op n decimalen (standaard 0)
        w.plafond()             rond af naar boven (geheel getal)
        w.vloer()               rond af naar beneden (geheel getal)
        w.plafond_0_vloer()     rond af richting 0 (geheel getal)
        w1.optellen(w2)         w1 + w2
        w1.aftrekken(w2)        w1 - w2
        w1.vermenigvuldigen(w2) w1 * w2
        w1.delen(w2)            w1 / w2
        w1.delen_aantal(w2)     afgerond naar beneden
        w1.delen_rest(w2)       restant na afronden naar beneden
        w.macht(n)              w ** n
        w.reciproke()           1 / w
        w.negatief()            -w
        w.exp()                 exponentieel: berekent e^w
        w.ln()                  natuurlijke logaritme (grondgetal e)
        w.log()                 logaritme met grondgetal 10
        w.wortel()              vierkantswortel
        w.wortel3()             kubieke wortel
        w.absoluut()            absolute waarde (altijd positief)
        w.teken()               positief getal: 1.0, nul: 0.0, negatief: -1.0 
        w.kopieer_teken(w2)     neem huidige, met het teken (+-) van w2
        w.is_positief(a)        stap functie: w<0 -> 0, w=0 -> a, w>0 -> 1 
        w.is_nan()              bepaalt of waarde een niet-getal is
        w.is_inf()              bepaalt of waarde oneindig is
    
    EENHEID TEKST
        gebruik getal achter standaard eenheid voor 'tot de macht' (bijv. mm3)
        gebruik / (maximaal één keer) om teller en noemer te introduceren
        gebruik * om eenheden te combineren (zowel in teller als noemer)
        bijvoorbeeld: "m3*kPa/s4*m"
    
    STANDAARD EENHEDEN          deze kan je combineren in een eenheid tekst
        dimensieloos            -
        massa                   ag fg pg ng mug mg cg g hg kg Mg Gg Tg Pg Eg
                                ton kton Mton ounce pound kip stone grain
        lengte                  am fm pm nm mum mm cm dm m dam hm km Mm Gm Tm
                                Pm Em in ft yard zeemijl mijl
        tijd                    as(.attos) fs ps ns mus ms cs ds s das hs ks
                                Ms Gs Ts Ps Es min(.minuut) h d j
        temperatuur             C K F  (als temperatuur in teller, samen met
                                andere eenheden, dan niet om te rekenen)
        hoek                    rad deg gon
        kracht                  N kN MN GN TN  (of massa*lengte/tijd^2)
        spanning                Pa kPa MPa GPa TPa  (of kracht/oppervlakte)
        moment                  Nm kNm MNm Nmm kNmm MNmm  (of kracht*lengte)
        oppervlakte             ca a ha  (of lengte^2)
        inhoud                  ml cl dl l dal hl kl gallon pint floz tbs tsp
                                bbl cup  (of lengte^3)
    
    BESCHIKBARE EIGENSCHAPPEN   voor snel toekennen van eenheid aan waarde
    <object>.<eigenschap>       bijvoorbeeld toekennen inhoud: w.dm3
    a ag am attos bbl C ca cg cl cl_d cl_h cl_j cl_min cl_s cm cm2 cm3 cm3_d
    cm3_h cm3_j cm3_min cm3_s cm4 cm_d cm_h cm_j cm_min cm_s cs cup d dal dam
    das deg dg dl dl_d dl_h dl_j dl_min dl_s dm dm2 dm3 dm3_d dm3_h dm3_j
    dm3_min dm3_s dm4 dm_d dm_h dm_j dm_min dm_s ds Eg Em Es F fg floz fm fs ft
    g gallon Gg Gm GN gon GPa grain Gs h ha hg hl hm hm2 hm3 hs inch K kg kip
    kl km km2 km3 km3_d km3_h km3_j km3_min km3_s km4 km_d km_h km_j km_min
    km_s kN kNm kNmm kN_m kN_mm kN_m2 kN_mm2 kPa ks kton l l_d l_h l_j l_min
    l_s m m2 m3 m3_d m3_h m3_j m3_min m3_s m4 Mg mg mijl minuut ml ml_d ml_h
    ml_j ml_min ml_s Mm mm mm2 mm3 mm3_d mm3_h mm3_j mm3_min mm3_s mm4 mm_d
    mm_h mm_j mm_min mm_s MN MNm MNmm MN_m2 MN_mm2 MPa Ms ms Mton mug mum mus
    m_d m_h m_j m_min m_s N ng Nm nm Nmm ns N_m N_mm N_m2 N_mm2 ounce Pa Pg pg
    pint Pm pm pound Ps ps rad s stone tbs Tg Tm TN ton TPa Ts tsp yard zeemijl
    
    


```python
W = pc.Waarde
print(f"12 dm + 58 cm = { (W(12).dm + W(58).cm).mm }")
print(f"pi radialen komt overeen met: { W(3.141592654, 'rad').deg }")
print(f"1 meter per 10 graden Celsius komt overen met: { W(1/10, 'm/C')['cm/F'] }")
```

    12 dm + 58 cm = 1780.0000000000002 mm
    pi radialen komt overeen met: 180.00000002350313 deg
    1 meter per 10 graden Celsius komt overen met: 5.5555555555555545 cm/F
    

## Lijst

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Lijst.print_help()
```

    
    +---------+
    |  Lijst  |
    +---------+
    
    Bevat een aantal getallen of Waarde objecten met allen dezelfde eenheid.
    
    AANMAKEN LIJST              eenheid van 1e component, geldt voor geheel
        l = Lijst(waarde1, waarde2, ...)          waarde: float, int of Waarde
        l = Lijst([waarde1, waarde2, ...])              
        l = Lijst(numpy_array)             array wordt indien nodig 1D gemaakt
        l2 = l.kopie()          maak een kopie (nieuw object) met zelfde eigenschappen 
    
    AANPASSEN EENHEID           omzetten van eenheid naar andere eenheid
        l.eenheid               huidige eenheid opvragen (tekst of None)
        l.eenheid = 'N/mm2'     eenheid aanpassen
        l.gebruik_eenheid('m')  eenheid aanpassen, retourneert object
        l.eh('m')               eenheid aanpassen, retourneert object
        l = l.N_mm2             kan voor een aantal standaard gevallen (zie lijst onderaan)
    
    OMZETTEN LIJST NAAR TEKST   resulteert in nieuw string object
        tekst = str(l)          of automatisch met bijvoorbeeld print(l)
        tekst = format(l, '.2f') format configuratie meegeven voor getal
              = l.format('.2f')
    
    MOGELIJKE BEWERKINGEN       resulteert in nieuw Lijst object
        l3 = l1 + l2            lijst optellen bij lijst
        l3 = l1 - l2            lijst aftrekken van lijst
        getal = l1 * l2         lijst vermenigvuldigen met lijst (inproduct)
        getal = l1 / l2         lijst delen door lijst (inverse inproduct)
        l2 = n * l1             getal vermenigvuldigen met lijst
        l2 = l1 * n             lijst vermenigvuldigen met getal
        l2 = n / l1             getal delen door lijst
        l2 = l1 / n             lijst delen door getal
        l2 = l1 ** n            lijst tot de macht een geheel getal
        waarde = abs(l1)        berekent lengte van lijst -> Waarde object
        getal = float(l1)       berekent lengte van lijst -> float object
        l2 = +l1                behoud teken
        l2 = -l1                verander teken (positief vs. negatief)
        for w in l1:            itereert en geeft float/Waarde object terug
        getal = len(l1)         geeft aantal elementen (dimensies) van lijst
    
    NUMPY BEWERKINGEN           gebruikt array object
        numpy_array = l1.array  retourneert Numpy array object
                                    (bevat allen getallen, zonder eenheid)
        getal = l1[2]           retourneert getal (zonder eenheid) op index
        numpy_array = l1[1:3]   retourneert Numpy array object vanuit slice
    
    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        l1 == l2                de totale lijst is gelijk aan
        l1 != l2                de totale lijst is niet gelijk aan
        l1 >  l2                de absolute waarde van lijst is groter dan
        l1 <  l2                de absolute waarde van lijst is kleiner dan
        l1 >= l2                de absolute waarde van lijst is groter dan of gelijk aan
        l1 <= l2                de absolute waarde van lijst is kleiner dan of gelijk aan
        l1 &  l2                eenheden zijn zelfde type
        
    WISKUNDIGE FUNCTIES         
        l.sin()                 sinus (alleen getallen en hoeken)
        l.cos()                 cosinus (alleen getallen en hoeken)
        l.tan()                 tangens (alleen getallen en hoeken)
        l.asin()                arcsinus (omgekeerde sin, alleen getallen)
        l.acos()                arccosinus (omgekeerde cos, alleen getallen)
        l.atan()                arctangens (omgekeerde tan, alleen getallen)
        l.sinh()                hyperbolische sinus (getallen en hoeken)
        l.cosh()                hyperbolische cosinus (getallen en hoeken)
        l.tanh()                hyperbolische tangens (getallen en hoeken)
        l.asinh()               arcsinus hyperb. (omgekeerde asinh, getallen)
        l.acosh()               arccosinus hyperb. (omgekeerde acosh, getallen)
        l.atanh()               arctangens hyperb. (omgekeerde atanh, getallen)
        l.afronden(n)           rond af op n decimalen (standaard 0)
        l.plafond()             rond af naar boven (geheel getal)
        l.vloer()               rond af naar beneden (geheel getal)
        l.plafond_0_vloer()     rond af richting 0 (geheel getal)
        l.som()                 de som van de elementen
        l.product()             het product van de elementen
        l.verschil()            lijst met verschillen tussen elementen
        l1.optellen(l2)         l1 + l2
        l1.aftrekken(l2)        l1 - l2
        l1.vermenigvuldigen(l2) l1 * l2
        l1.delen(l2)            l1 / l2
        l1.delen_aantal(l2)     afgerond naar beneden
        l1.delen_rest(l2)       restant na afronden naar beneden
        l.macht(n)              l ** n
        l.reciproke()           1 / l
        l.negatief()            -l
        l1.kruisproduct(l2)     l1 x l2: staat loodrecht op vector l1 en l2
        l1.inwendigproduct(l2)  l1 . l2: is |l1| * |l2| * cos(theta)
        l.exp()                 exponentieel: berekent e^l
        l.ln()                  natuurlijke logaritme (grondgetal e)
        l.log()                 logaritme met grondgetal 10
        l.bijsnijden(min, max)  snij alle elementen af tot minmax bereik
        l.wortel()              vierkantswortel
        l.wortel3()             kubieke wortel
        l.absoluut()            absolute waarde (altijd positief)
        l.teken()               positief getal: 1.0   negatief: -1.0 
        l.kopieer_teken(l2)     neem huidige, met het teken (+-) van l2
        l.is_positief(a)        stap functie: l<0 -> 0, l=0 -> a, l>0 -> 1 
        l.verwijder_nan()       verwijder niet-getallen (not a number)
        l.getal_nan_inf()       vervang: nan=0, inf=1.7e+308 (heel groot)
        l.gemiddelde()          bepaalt het gemiddelde
        l.stdafw_pop()          bepaalt standaardafwijking voor populatie
        l.stdafw_n()            bepaalt standaardafwijking steekproef
        l.mediaan()             bepaalt de mediaan
        l.percentiel(perc)      percentage: getal tussen 0 en 100
        l.correlatie(l2)        bepaalt correlatie matrix
        l.sorteer()             sorteert een lijst van klein naar groot
        l.omdraaien()           draai de volgorde van de lijst om
        l.is_nan()              bepaalt per element of een niet-getal is
        l.is_inf()              bepaalt per element of oneindig is
        l1.gelijk(l2)           per element: w1 == w2
        l1.niet_gelijk(l2)      per element: w1 != w2
        l1.groter(l2)           per element: w1 > w2
        l1.groter_gelijk(l2)    per element: w1 >= w2
        l1.kleiner(l2)          per element: w1 < w2
        l1.kleiner_gelijk(l2)   per element: w1 <= w2
        l.alle()                kijkt of alle elementen True zijn
        l.sommige()             kijkt of er minimaal 1 element True is
        l.niet_alle()           kijkt of er minimaal 1 element False is
        l.geen()                kijkt of alle elementen False zijn
        l.waar()                zet lijst om in list met True/False
        
    BESCHIKBARE EIGENSCHAPPEN   voor snel toekennen van eenheid aan waarde
    <object>.<eigenschap>       bijvoorbeeld toekennen inhoud: v.dm3
    a ag am attos bbl C ca cg cl cl_d cl_h cl_j cl_min cl_s cm cm2 cm3 cm3_d
    cm3_h cm3_j cm3_min cm3_s cm4 cm_d cm_h cm_j cm_min cm_s cs cup d dal dam
    das deg dg dl dl_d dl_h dl_j dl_min dl_s dm dm2 dm3 dm3_d dm3_h dm3_j
    dm3_min dm3_s dm4 dm_d dm_h dm_j dm_min dm_s ds Eg Em Es F fg floz fm fs ft
    g gallon Gg Gm GN gon GPa grain Gs h ha hg hl hm hm2 hm3 hs inch K kg kip
    kl km km2 km3 km3_d km3_h km3_j km3_min km3_s km4 km_d km_h km_j km_min
    km_s kN kNm kNmm kN_m kN_mm kN_m2 kN_mm2 kPa ks kton l l_d l_h l_j l_min
    l_s m m2 m3 m3_d m3_h m3_j m3_min m3_s m4 Mg mg mijl minuut ml ml_d ml_h
    ml_j ml_min ml_s Mm mm mm2 mm3 mm3_d mm3_h mm3_j mm3_min mm3_s mm4 mm_d
    mm_h mm_j mm_min mm_s MN MNm MNmm MN_m2 MN_mm2 MPa Ms ms Mton mug mum mus
    m_d m_h m_j m_min m_s N ng Nm nm Nmm ns N_m N_mm N_m2 N_mm2 ounce Pa Pg pg
    pint Pm pm pound Ps ps rad s stone tbs Tg Tm TN ton TPa Ts tsp yard zeemijl
    
    


```python
pc.Lijst(0, 200, 1).eh('cm')
```




    Lijst(Waarde(0.0, 'cm'), Waarde(200.0, 'cm'), Waarde(1.0, 'cm'))



## Data
[terug naar inhoudsopgave](#Inhoud)


```python
pc.Data.print_help()
```

    
    +--------+
    |  Data  |
    +--------+
    
    Een Pandas DataFrame waarbij eigenschappen een eenheid kunnen hebben.
    
    AANMAKEN DATA  
        d = Data({'eigenschap1': 'eenheid1',           als eenheid dimensieloos:
                  'eigenschap2': 'eenheid2'})                  '-', '' of None
                  
    EIGENSCHAPPEN
        d.eigenschappen           lijst met aanwezige kolomnamen
        d.eenheden                lijst met eenheden die bij kolommen horen
        d.df                      Pandas DataFrame object     
        
    TOEVOEGEN DATA REGEL    in onderstaande gevallen: 4 eigenschappen (kolommen)
        d.toevoegen([7,5,3,1])             een Python list object
        d.toevoegen(4,5,6,7)               losse argumenten
        d.toevoegen(pc.Lijst(4,9,6,70))    een Lijst object
        d.toevoegen((14,15,16,17))         een Python tuple object
    
    OPHALEN DATA EIGENSCHAP       
        d['eigenschap1']          een Lijst object
        d.eigenschap1             indien naam eigenschap ook valide Python name
        d[0]                      Python list met waardes van 1e invoer (rij)
        d[3:8]                    Python list met waardes (ook Python list)
                                                    van 4e t/m 8e invoer (rijen)
        d[::2]                    Python list met alle oneven rijnummers
        d[:, 1:3]                 Python list met 2e en 3e kolom
                                                  (alleen waarden, geen eenheid)
    
    


```python
d = pc.Data({
    'x': 'mm',
    'N': 'kN',
    'V': 'kN',
    'M': 'kNm',
})
d.toevoegen([7,5,3,1])
d.toevoegen(4,5,6, 1)
d.toevoegen(pc.Lijst(4,9,6,70))
d.toevoegen((14,15,16,17))
print(d)
print()
print('M is:', d.M)
```

         x    N    V     M
        mm   kN   kN   kNm
    0    7    5    3     1
    1    4    5    6     1
    2  4.0  9.0  6.0  70.0
    3   14   15   16    17
    
    M is: (1.0, 1.0, 70.0, 17.0) kNm
    

## Knoop

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Knoop.print_help()
```

    
    +---------+
    |  Knoop  |
    +---------+
    
    Bevat een lijst van getallen of Waarde (x, y, en/of z) met lengte eenheid.
    
    AANMAKEN KNOOP              eenheid van 1e component, geldt voor geheel
        k = Knoop([x_waarde, y_waarde, z_waarde])   kan oneindig veel dimensies
    
    AANPASSEN EENHEID           omzetten van eenheid naar andere eenheid
        k.eenheid               huidige eenheid opvragen (tekst of None)
        k.eenheid = 'N/mm2'     eenheid aanpassen
        k.gebruik_eenheid('m')  zelfde als bovenstaande, retourneert object
    
    OMZETTEN KNOOP NAAR TEKST   resulteert in nieuw string object
        tekst = str(k)          of automatisch met bijvoorbeeld print(w)
        tekst = format(k,'.2f') format configuratie meegeven voor getal
    
    MOGELIJKE BEWERKINGEN       resulteert in nieuw Knoop object
        k3 = k1 + k2            knoop optellen bij knoop
        k3 = k1 - k2            knoop aftrekken van knoop
        k2 = n * k1             getal vermenigvuldigen met knoop
        k2 = k1 * n             knoop vermenigvuldigen met getal
        k2 = n / k1             getal delen door knoop
        k2 = k1 / n             knoop delen door getal
        k2 = +k1                behoud teken
        k2 = -k1                verander teken (positief vs. negatief)
        for w in k1:            itereert en geeft float/Waarde object terug
        Waarde/getal = k1.x     retourneert 1e element als Waarde object
        Waarde/getal = k1.y     retourneert 2e element als Waarde object
        Waarde/getal = k1.z     retourneert 3e element als Waarde object
        getal = len(k1)         geeft aantal elementen (dimensies) van knoop
    
    NUMPY BEWERKINGEN           gebruikt array object
        numpy_array = k1.array  retourneert Numpy array object
                                    (bevat allen getallen, zonder eenheid)
        getal = k1[2]           retourneert getal (zonder eenheid) op index
        numpy_array = k1[1:3]   retourneert Numpy array object vanuit slice
    
    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        k1 == k2                is gelijk aan
        k1 != k2                is niet gelijk aan
        k1 &  k2                eenheden zijn zelfde type
    
    


```python
k1 = pc.Knoop(20, 20, 100).gebruik_eenheid('cm')
k2 = pc.Knoop(0, 0.8, 1.5).gebruik_eenheid('m')
k3 = pc.Knoop(0, 0, 1000).gebruik_eenheid('mm')

print(f'k2 heeft een x-waarde [{k2.x}], een y-waarde [{k2.y}] en een z-waarde [{k2.z}]')
```

    k2 heeft een x-waarde [0.0 m], een y-waarde [0.8 m] en een z-waarde [1.5 m]
    

## Lijn

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Lijn.print_help()
```

    
    +--------+
    |  Lijn  |
    +--------+
    
    Bevat een collectie met knopen, waartussen zich rechte lijnen bevinden.
    
    AANMAKEN LIJN               invoeren van één of meedere Knoop objecten
        Lijn(Knoop(Waarde(1).cm, Waarde(2).cm)))    begin Knoop object
        Lijn([1,2]) of Lijn((1,2))                  alleen begincoordinaat
        Lijn((1,2), (3,4), (5,6))                   alle knoopcoordinaten
    
    AANPASSEN EENHEID
        l = Lijn((1,2), (3,4))
        l.eenheid               opvragen huidige eenheid; in dit geval None
        l.eenheid = 'm'         alle waarden in alle knoopobjecten naar 'm'
        l.gebruik_eenheid('m')  zelfde als bovenstaande, retourneert object
    
    OMZETTEN LIJN NAAR TEKST    resulteert in nieuw string object
        tekst = str(l)          of automatisch met bijvoorbeeld print(l)
        tekst = format(l,'.2f') format configuratie meegeven voor getal
    
    VERLENGEN LIJN              vanuit laatste knoop (of enige beginknoop)
        l.lijn_recht(naar=(3,4))
            rechte lijn naar een nieuwe knoop
    
        l.lijn_bezier(richting=(3,4), naar=(5,6), stappen=100)
            (kwadratische) Bezier kromme (met één richtingspunt) naar nieuwe
            knoop waarbij de kromme lijn omgezet wordt in aantal (stappen)
            rechte lijnen; standaard 100 stappen
    
        l.lijn_cirkelboog(middelpunt=(3,4), gradenhoek=-90, stappen=100)
            cirkelboog met opgegeven cirkel middelpunt over aantal opgegeven
            graden (waarbij 360 is gehele cirkel tekenen; positief is tegen
            klok in; negatief getal is met de klok mee) waarbij kromme lijn
            omgezet wordt in aantal rechte lijnen; standaard 100 stappen
    
    TRANSFORMEREN LIJN
        l.transformeren(       # standaard zijn alle parameters None
            rotatiepunt=[0,0], # xy Knoop/list; als None dan zwaartepunt vorm
            rotatiehoek=20,    # in graden, positief is tegen de klok in
            schaalfactor=2,  # Waarde/getal: vergrootfactor t.o.v. rotatiepunt
            schaalfactor=[2,3],# of Lijst/list met x-schaalfactor en y-factor
            schaalfactor=[1,-1],# verticaal spiegelen
            schaalfactor=[-1,1],# horizontaal spiegelen
            schaalfactor=[-5,3],# bovenstaande combineren
            translatie=[10,5], # xy verschuiven (na roteren en schalen)
        )
    
    MOGELIJKE BEWERKINGEN
        waarde = abs(l)         berekent lengte lijnstukken -> Waarde object
        getal = float(l)        berekent lengte lijnstukken -> float object
        for w in v1:            itereert en geeft Knoop object terug
        getal = len(v1)         geeft aantal knopen terug
    
    NUMPY BEWERKINGEN               gebruikt array object
        2D numpy_array = l1.array   retourneert volledige Numpy array object
                                      (bevat allen getallen, zonder eenheid)
        1D_numpy_array = l1[2]      retourneert knoopcoordinaten op index
        2D_numpy_array = l1[1:3]    retourneert knoopcoordinaten vanuit slice
    
    WAARDEN VERGELIJKEN         resulteert in een boolean (True/False)
        l1 == l2                is gelijk aan
        l1 != l2                is niet gelijk aan
        l1 &  l2                eenheden zijn zelfde type
    
    EXTRA OPTIES
        l.plot()                plot simpele 2D weergave van lijn
        l.plot3D()              plot simpele 3D weergave van lijn
    
        Lijn((4, -5), (-10, 10)).lijn_cirkelboog(middelpunt=(0,0),
            gradenhoek=+220, stappen=50).lijn_recht(naar=(4, 10)).lijn_bezier(
            richting=(-10,-4), naar=(4, -5)).plot()
    
    


```python
pc.Lijn(k1, k2, k3).plot3D()
```


    
![png](output_18_0.png)
    


## Vorm

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Vorm.print_help()
```

    
    +--------+
    |  Vorm  |
    +--------+
    
    Betreft een meetkundig 2D vorm met bijbehorende eigenschappen.
    
    AANMAKEN VORM
        v1 = Vorm(Lijn)                 invoeren van één Lijn object
        v2 = Vorm([(0,0),(1,1),(1,0)])  direct invoeren knoopcoordinaten
    
    EENHEID
        v.eenheid       opvragen huidige eenheid; of None als alleen getal
        v.eenheid = 'm' alle waarden in alle knoopobjecten naar 'm'
        v.gebruik_eenheid('m')   zelfde als bovenstaande, retourneert object
    
    EIGENSCHAPPEN       naam + '_'  -->  Waarde object i.p.v. getal
        v.O             omtrek   (bijv. v.O_ geeft omtrek Waarde met eenheid)
        v.A             oppervlakte
        v.xmin v.xmax   minimum en maximum x-waarde
        v.ymin v.ymax   minimum en maximum y-waarde
        v.ncx  v.ncy    x- en y-waarde normaalkrachtencetrum (zwaartepunt)
        v.Ixx  v.Iyy    oppervlakte traagheidsmoment in x- en y-richting
        v.Ixy           traagheidsproduct (is 0 voor symmetrische vormen)
        v.I1   v.I2     hoofdtraagheidsmomenten (1 sterke richting, 2 zwakke)
        v.alpha         hoek (tegen klok in) hoofdtraagheidsassen
        v.Wxmin v.Wxmax weerstandsmoment voor vezel x-minimaal en x-maximaal
        v.Wymin v.Wymax weerstandsmoment voor vezel y-minimaal en y-maximaal
        v.kxmin v.kxmax laagste/hoogste x-waarde van kern
        v.kymin v.kymax laagste/hoogste y-waarde van kern
    
    KNOOP COORDINATEN
        v.array                 Numpy array met x/y coordinaten
        v.array_gesloten        zelfde, met kopie 1e knoop aan het einde
        v.kern_array            Numpy array met x/y coordinaten van kern
        v.kern_array_gesloten   zelfde, met kopie 1e knoop aan het einde
    
    LIJN OBJECT
        v.lijn        genereert een Lijn object van vorm omtrek (gesloten)
    
    BEWERKINGEN
        v[3]          subset Numpy array object met getallen (zonder eenheid)
        len(v)        aantal knopen
        for k in v:   itereert over knopen, geeft Knoop object (met eenheid)
    
    OVERIG
        v.plot()                Matplotlib plot met vormeigenschappen
        v.print_eigenschappen() print overzicht van eigenschappen
        v.print_eigenschappen(knopen=True)  zelfde, met lijst van knopen
    
    


```python
v1 = pc.Vorm(pc.Lijn([-50,-40], [-40, -40], [-30, 15], [30, 15], [40, -40], [50,-40], [50,20], [0, 40], [-50, 20]).transformeren(
          rotatiepunt=None, # bij None: neemt standaard zwaartepunt
          rotatiehoek=45, # graden tegen de klok in
          schaalfactor=[-2, 1], # vergroten om rotatiepunt; negatief:spiegelen
          translatie=[50, -120] # verplaatsing
    ).gebruik_eenheid('mm'))
v1.plot()
v1.print_eigenschappen()
print(f'het grootste hoofdtraagheidsmoment is: {v1.I1:.2e} mm4')
```


    
![png](output_21_0.png)
    


    
           O = 658.439 mm
           A = 6300.000 mm2
        xmin = -86.184 mm
        xmax = 140.091 mm
        ymin = -181.795 mm
        ymax = -68.658 mm
         ncx = 50.000 mm
         ncy = -113.704 mm
         Ixx = 20491327.160 mm4
         Iyy = 5122831.790 mm4
         Ixy = -5004336.420 mm4
          I1 = 21977196.459 mm4
          I2 = 3636962.492 mm4
       alpha = -16.537 deg
       Wxmin = 150468.470 mm3
       Wxmax = 227452.339 mm3
       Wymin = 37617.118 mm3
       Wymax = 56863.085 mm3
       kxmin = -36.104 mm
       kxmax = 23.884 mm
       kymin = -36.104 mm
       kymax = 23.884 mm
    
    het grootste hoofdtraagheidsmoment is: 2.20e+07 mm4
    

## Rechthoek

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Rechthoek.print_help()
```

    
    +-------------+
    |  Rechthoek  |
    +-------------+
    
    Creeert een rechthoekig Vorm object.
    
    AANMAKEN RECHTHOEK
        r = Rechthoek(breedte=Waarde(300).mm, hoogte=Waarde(500).mm)
        
    Verder zijn alle eigenschappen van toepassing als van een Vorm object.
    
    


```python
pc.Rechthoek(breedte=30, hoogte=50).plot()
```


    
![png](output_24_0.png)
    


## Cirkel

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Cirkel.print_help()
```

    
    +----------+
    |  Cirkel  |
    +----------+
    
    Creeert een cirkelvormig Vorm object.
    
    AANMAKEN CIRKEL
        c = Cirkel(straal=Waarde(3).mm)
        
    Vormeigenschappen worden exact bepaald, daar waar een Vorm object een ronde
    rand benadert met kleine rechte lijnen.
    
    Verder zijn alle eigenschappen en methoden van toepassing als van een
    Vorm object.
    
    


```python
pc.Cirkel(straal=pc.Waarde(1).dm).gebruik_eenheid('m').plot()
```


    
![png](output_27_0.png)
    


## Figuur
[terug naar inhoudsopgave](#Inhoud)


```python
pc.Figuur.print_help()
```

    
    +----------+
    |  Figuur  |
    +----------+
    
    Tekent een figuur met behulp van matplotlib bibliotheek.
    
    WERKWIJZE                   plaats functies achter elkaar
    f = Figuur(                 # configuratie
            breedte=7,
            hoogte=7,
        ).lijn(                 # onderdeel 1
            coordinaten=((2, 0), (3, 7)),
        ).fx(                   # onderdeel 2  etc.
            functie = lambda x: x**2,
            x = (-2, 3),
        )                       
    
    LIJN OBJECT             in plaats van tuple/list met coordinaten,
                            mag ook Lijn object invoeren
        Figuur().punt(
            coordinaten=Lijn([1,2],[3,4],[5,6])
        )
    
    CONFIGURATIE
        Figuur(
            breedte=7,
            hoogte=7,
            raster=True,
            legenda=True,
            titel='Kunst',
            x_as_titel='variabele $x$',
            y_as_titel='resultaat $y$',
            gelijke_assen=True,
            verberg_assen=False,
            x_as_log=False,
            y_as_log=False,
        )
    
    ONDERDELEN
        .lijn(
            coordinaten=((2, 0), (3, 7), (-2, 4), (2, 0)),
            breedte=3,
            kleur='red',   # None is auto kleur
            vullen=False,
            arcering='/',
            naam='dit is een lijn',
        )
    
        .punt(
            coordinaten=((2, 0), (3, 7), (-2, 4)),
            breedte=10,
            kleur='gold',   # None is auto kleur
            stijl='>',
            naam='dit zijn punten',
        )
    
        .tekst(
            coordinaten=((2, 0), (3, 7), (-2, 4)),
            teksten=('punt 1', 'punt 2', 'punt 3'),
            kleur='brown',   # None is auto kleur
            tekst_grootte='large', # {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
            tekst_font='sans-serif', # {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'}
            tekst_stijl='normal', # {'normal', 'italic', 'oblique'}
            tekst_gewicht='bold', # {'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'}
            hor_uitlijnen='center', # {'center', 'right', 'left'}
            vert_uitlijnen='center', # {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
            roteren=30, # in graden
        )
    
        .kolom(
            coordinaten=((3, 8), (6, 4), (8, 1)),
            kleur='pink',   # None is auto kleur
            breedte=0.4,
            lijn_kleur='peru',
            lijn_breedte=2,
            naam='bar plot',
        )
    
        .fx(
            functie = lambda x: x**2 + 3*pc.sin(x),
            x = (-2, 3),
            breedte = 2,
            kleur = 'green',   # None is auto kleur
            naam = 'sinus parabool',
        )
        
    WEERGAVE FIGUUR
        f.plot()                # plot direct in notebook/console
        f.plot_venster()        # plot in een popup venster
    
    OVERIG
        f.volgende_kleur        # gebruik deze eigenschap om verschillende automatische kleuren te gebruiken
        f.png_url               # data url encoded
        f.png_html              # HTML IMG code van PNG afbeelding (data url encoded)
        f.svg_html              # SVG code voor inline HTML gebruik
        f.bewaar_als_png()      # vraag bestandsnaam om op te slaan als PNG
        f.bewaar_als_svg()      # vraag bestandsnaam om op te slaan als SVG
    
    


```python
lijn1 = pc.Lijn((2, 2), (3, 7), (-2, 4), (1, 0)).transformeren(
            rotatiehoek=45,
            schaalfactor=1.8,
       )

f1 = pc.Figuur(
        breedte=7,
        hoogte=7,
        raster=True,
        legenda=True,
        titel='Kunst',
        x_as_titel='variabele $x$',
        y_as_titel='resultaat $y$',
        gelijke_assen=True,
        verberg_assen=False,
        x_as_log=False,
        y_as_log=False,
    ).lijn(
        coordinaten=lijn1,
        breedte=3,
        kleur=None,  # auto kleur
        vullen=False,
        arcering='/',
        naam='dit is een lijn',
    ).punt(
        coordinaten=lijn1,
        breedte=10,
        kleur=None,  # auto kleur
        stijl='>',
        naam='dit zijn punten',
    ).tekst(
        coordinaten=lijn1,
        teksten=('punt 1', 'punt 2', 'punt 3'),
        kleur=None,  # auto kleur
        tekst_grootte='large', # {'xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'}
        tekst_font='sans-serif', # {FONTNAME, 'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace'}
        tekst_stijl='normal', # {'normal', 'italic', 'oblique'}
        tekst_gewicht='bold', # {'ultralight', 'light', 'normal', 'regular', 'book', 'medium', 'roman', 'semibold', 'demibold', 'demi', 'bold', 'heavy', 'extra bold', 'black'}
        hor_uitlijnen='center', # {'center', 'right', 'left'}
        vert_uitlijnen='center', # {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
        roteren=30, # in graden
    ).kolom(
        coordinaten=((3, 8), (6, 4), (8, 1)),
        kleur=None,  # auto kleur
        breedte=0.4,
        lijn_kleur='peru',
        lijn_breedte=2,
        naam='bar plot',
    ).fx(
        functie=lambda x: x**2 + 3*pc.sin(x),
        x=(-2, 3),
        breedte=2,
        kleur=None,  # auto kleur
        naam='sinus parabool',
    )
```


    
![png](output_30_0.png)
    


## Materiaal

[terug naar inhoudsopgave](#Inhoud)


```python
pc.Materiaal.print_help()
```

    
    +-------------+
    |  Materiaal  |
    +-------------+
    
    Betreft een materiaal met diverse eigenschappen.
    
    AANMAKEN MATERIAAL
        m = Materiaal(E=Waarde(210, 'GPa'),     # elasticiteitsmodulus
                      G=Waarde(75, 'GPa'),      # glijdings(schuif)modulus
                      v=Waarde(0.4),            # dwarscontractiecoëfficiënt
                                                               (Poisson factor)
                      sm=Waarde(7850, 'kg/m3'), # soortelijke massa (dichtheid)
                      sg=Waarde(78.5, 'kN/m3')) # soortelijk gewicht
        
    RELATIE E, G EN v
        Indien E en v bekend zijn, dan wordt G zelf bepaald: G = E/(2(1+v))
        Indien E en G bekend zijn, dan wordt v zelf bepaald: v = (E/2G)-1
        Alledrie grootheden kunnen handmatig worden overschreven.
        
    OPVRAGEN EN AANPASSEN MATERIAALEIGENSCHAPPEN
        m.E                             # retourneert Waarde object
        m.E = Waarde(180).GPa           # past waarde E aan
    
    


```python
S235 = pc.Materiaal(
    E=W(210).GPa,
    G=W(75).GPa,
    sm=W(7850)['kg/m3'],
    sg=W(78.5)['kN/m3'],
    )
print(f'dwarscontractiecoëfficiënt is: {S235.v}')
```

    dwarscontractiecoëfficiënt is: 0.3999999999999999
    

## Functies

[terug naar inhoudsopgave](#Inhoud)

Naast bovenstaande pyco objecten, zijn er ook algemene pyco functies en eigenschappen beschikbaar. Deze beginnen altijd met een kleine letter.


```python
pc.functies_print_help()
```

    +-------------------------------------------+
    |  algemene pyco functies en eigenschappen  |
    +-------------------------------------------+
    
    ALGEMEEN GEBRUIK VAN FUNCTIES         alle namen met () erachter zijn functies
        pc.wortel(9) == 3.0               direct aan te roepen vanuit pc object
        
    ALGEMEEN GEBRUIK VAN EIGENSCHAPPEN
        pc.pi == 3.141592653589793        direct aan te roepen vanuit pc object
    
    WISKUNDIGE FUNCTIES                   (geïmporteerd uit Numpy module)
        invoerwaarden:  int, float, np.array, Waarde of Lijst
        sin(x)                            sinus
        cos(x)                            cosinus
        tan(x)                            tangens
        asin(x)                           arcsinus (omgekeerde sin)
        acos(x)                           arccosinus (omgekeerde cos)
        atan(x)                           arctangens (omgekeerde tan)
        hypot(a, b)                       hypotenuse (c in: a^2 + b^c = c^2)
        graden(rad)                       van radialen naar graden
        radialen(deg)                     van graden naar radialen
        sinh(x)                           hyperbolische sinus
        cosh(x)                           hyperbolische cosinus
        tanh(x)                           hyperbolische tangens
        asinh(x)                          arc hyperb. sinus (omgekeerde sinh)
        acosh(x)                          arc hyperb. cosinus (omgekeerde cosh)
        atanh(x)                          arc hyperb. tangens (omgekeerde tanh)
        afronden(x, n)                    rond af op n decimalen (standaard 0)
        plafond(x)                        rond af naar boven (geheel getal)
        vloer(x)                          rond af naar beneden (geheel getal)
        plafond_0_vloer(x)                rond af richting 0 (geheel getal)
        som(lijst)                        de som van de elementen
        product(lijst)                    het product van de elementen
        verschil(lijst)                   lijst met verschillen tussen elementen
        optellen(a, b)                    a + b
        aftrekken(a, b)                   a - b
        vermenigvuldigen(a, b)            a * b
        delen(a, b)                       a / b
        delen_aantal(a, b)                delen afgerond naar beneden
        delen_rest(a, b)                  restant na afronden naar beneden
        macht(a, n)                       a ** n
        reciproke(x)                      1 / x
        negatief(x)                       -x
        kruisproduct(lijst_a, lijst_b)    a x b: staat loodrecht op vector a en b
        inwendigproduct(lijst_a, lijst_b) a . b: is |a| * |b| * cos(theta)
        exp(x)                            exponentieel: berekent e^x
        ln(x)                             natuurlijke logaritme (grondgetal e)
        log(x)                            logaritme met grondgetal 10
        kleinste_gemene_veelvoud(a, b)    kleinste gemene veelvoud: a=12 b=20: 60
        grootste_gemene_deler(a, b)       grootste gemene deler: a=12 b=20: 4
        min(lijst)                        bepaalt minimum waarde lijst
        max(lijst)                        bepaalt maximum waarde lijst
        bijsnijden(lijst, min, max)       snij alle elementen af tot minmax bereik
        wortel(x)                         vierkantswortel
        wortel3(x)                        kubieke wortel
        absoluut(x)                       absolute waarde (altijd positief)
        teken(x)                          positief getal: 1.0   negatief: -1.0 
        kopieer_teken(a, b)               neem getal a, met het teken (+-) van b
        is_positief(a, b)                 stap functie:a<0 -> 0, a=0 -> b, a>0 -> 1 
        verwijder_nan(lijst)              verwijder niet-getallen (not a number)
        getal_nan_inf(lijst)              vervang: nan=0, inf=1.7e+308 (heel groot)
        interpoleer(x, array_x, array_y)  interpoleer x in y; array_x MOET oplopen
        van_totmet_n(van, tot_met, n)     genereert vast aantal getallen (incl. t/m)
        van_tot_stap(van, tot, stap)      genereert vaste stappen (excl. tot)
        gemiddelde(lijst)                 bepaalt het gemiddelde
        stdafw_pop(lijst)                 bepaalt standaardafwijking voor populatie
        stdafw_n(lijst)                   bepaalt standaardafwijking steekproef
        mediaan(lijst)                    bepaalt de mediaan
        percentiel(lijst, percentage)     percentage getal tussen 0 en 100
        correlatie(lijst_a, lijst_b)      bepaalt correlatie matrix
        sorteer(lijst)                    sorteert een lijst van klein naar groot
        omdraaien(lijst)                  draai de volgorde van de lijst om
        is_nan(x)                         bepaalt of waarde een niet-getal is
        is_inf(x)                         bepaalt of waarde oneindig is
        gelijk(lijst_a, lijst_b)          per element kijken of waarden gelijk zijn
        niet_gelijk(lijst_a, lijst_b)     per element kijken of waarden gelijk verschillen
        groter(lijst_a, lijst_b)          per element kijken of waarde groter dan
        groter_gelijk(lijst_a, lijst_b)   idem, maar dan ook gelijk
        kleiner(lijst_a, lijst_b)         per element kijken of waarde kleiner dan
        kleiner_gelijk(lijst_a, lijst_b)  idem, maar dan ook gelijk
        alle(lijst)                       kijkt of alle elementen True zijn
        sommige(lijst)                    kijkt of er minimaal 1 element True is
        niet_alle(lijst)                  kijkt of er minimaal 1 element False is
        geen(lijst)                       kijkt of alle elementen False zijn
        of(a, b)                          kijkt of a of b True is
        en(a, b)                          kijkt of a en b True is
        niet(x)                           omdraaien van True naar False en andersom
        xof(a, b)                         True als a of b True is, en niet beide
        
    WISKUNDIGE EIGENSCHAPPEN              (gebaseerd op Numpy module)
        nan                               float die geen getal is (not a number)
        inf                               oneindig groot
        pi                                3.141592653589793
        e                                 2.718281828459045
    


```python
l = pc.Lijst(3, 4, 7).mm
print(f"het gemiddelde van lijst l is: {pc.gemiddelde(l)}")
```

    het gemiddelde van lijst l is: 4.666666666666667 mm
    
