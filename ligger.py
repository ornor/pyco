import pyco.toepassing as pycot

lg = pycot.Ligger()

lg.knoop_eenheid = 'm'
lg.knoop('k', [0, 2, 6, 10])

lg.staaf('s1', 'k1', 'k2')
lg.staaf('s2', 'k2', 'k3')
lg.staaf('s3', 'k3', 'k4')

print(lg.knopen)
print(lg.staven)
