import unittest

import numpy as np

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde
Knoop = doc.model.Knoop
Lijn = doc.model.Lijn
Vorm = doc.model.Vorm

class TestVorm(unittest.TestCase):

    fn = Vorm([(0,0), (1,0), (0,1)]).fn

    def test_fn_punt_aan_linker_zijde(self):
        assert self.fn.punt_aan_linker_zijde((3,4),(5,6), (4,10))
        assert self.fn.punt_aan_linker_zijde((0,0),(0,5), (-4,10))
        assert self.fn.punt_aan_linker_zijde((0,0),(5,0), (2,2))

    def test_fn_punt_aan_rechter_zijde(self):
        assert self.fn.punt_aan_rechter_zijde((3,4),(5,6), (4,1))
        assert self.fn.punt_aan_rechter_zijde((0,0),(0,5), (4,10))
        assert self.fn.punt_aan_rechter_zijde((0,0),(5,0), (2,-2))

    def test_fn_punt_op_lijn(self):
        assert self.fn.punt_op_lijn((3,4),(5,6), (4,5))
        assert not self.fn.punt_op_lijn((3,4),(5,6), (1,2))
        assert not self.fn.punt_op_lijn((3,4),(5,6), (6,7))
        assert self.fn.punt_op_lijn((0,0),(0,5), (0,2))
        assert not self.fn.punt_op_lijn((0,0),(0,5), (0,-2))
        assert not self.fn.punt_op_lijn((0,0),(0,5), (0,10))
        assert self.fn.punt_op_lijn((0,0),(5,0), (2,0))
        assert not self.fn.punt_op_lijn((0,0),(5,0), (-2,0))
        assert not self.fn.punt_op_lijn((0,0),(5,0), (10,0))

    def test_fn_lijn_raakt_lijn(self):
        # kruisen diagonale lijnen
        assert self.fn.lijn_raakt_lijn((0,0),(10,10), (0,10),(10,0))
        assert self.fn.lijn_raakt_lijn((10,10),(0,0), (0,10),(10,0))
        assert self.fn.lijn_raakt_lijn((0,0),(10,10), (10,0),(0,10))
        assert self.fn.lijn_raakt_lijn((10,10),(0,0), (10,0),(0,10))
        # uiteinde op andere lijn
        assert self.fn.lijn_raakt_lijn((5,5),(0,0), (10,0),(0,10))
        assert self.fn.lijn_raakt_lijn((10,10),(5,5), (10,0),(0,10))
        assert self.fn.lijn_raakt_lijn((10,10),(0,0), (5,5),(0,10))
        assert self.fn.lijn_raakt_lijn((10,10),(0,0), (10,0),(5,5))
        # l1 en/of l2 is horizontaal/verticaal
        assert self.fn.lijn_raakt_lijn((0,5),(10,5), (0,10),(10,0))
        assert self.fn.lijn_raakt_lijn((5,0),(5,10), (0,10),(10,0))
        assert self.fn.lijn_raakt_lijn((0,0),(10,10), (0,5),(10,5))
        assert self.fn.lijn_raakt_lijn((0,0),(10,10), (5,0),(5,10))
        assert self.fn.lijn_raakt_lijn((0,5),(10,5), (5,0),(5,10))
        # een aantal negatieve checks
        assert not self.fn.lijn_raakt_lijn((0,0),(4,4), (0,10),(10,0))
        assert not self.fn.lijn_raakt_lijn((0,0),(4,4), (10,0),(0,-0.0001))
        assert not self.fn.lijn_raakt_lijn((0,0),(0,2), (0,3),(0,5))
        assert not self.fn.lijn_raakt_lijn((0,0),(2,0), (3,0),(5,0))

    def test_fn_bereken_hoek(self):
        assert self.fn.bereken_hoek((0,10), (0,0), (10,0)) == 270
        assert self.fn.bereken_hoek((0,10), (0,0), (10,0), True) == 90
        assert self.fn.bereken_hoek((-10,0), (0,0), (10,0)) == 180
        assert self.fn.bereken_hoek((5,5), (0,0), (10,0), True) == 45
        assert self.fn.bereken_hoek((10,0), (0,0), (10,0)) == 0

    def test_Vorm(self):
        self.assertRaises(TypeError, lambda: Lijn('str', 'str'))
        assert Lijn(Knoop(1, 2), Knoop(3, 4)) == Lijn([Knoop(1, 2), Knoop(3, 4)])




v1 = Vorm(Lijn(
        (4, -5), (-10, 10)
    ).lijn_cirkelboog(
        middelpunt=(0,0),
        gradenhoek=+220
    ).lijn_recht(
        naar=(4, 10)
    ).lijn_bezier(
        richting=(-10,-4),
        naar=(4, -5)
    ).transformeren(
        rotatiehoek=30,
        translatie=[15, 5],
    ))
v1.plot()
v1.print_eigenschappen()


v2 = Vorm([[0,0], [0,10], [4,10], [4,7], [6,7], [6,10], [10,10], [10,0]])
v2.plot()
v2.print_eigenschappen()


v3= Vorm(Lijn([-1,0]).lijn_cirkelboog(middelpunt=(0,0), gradenhoek=360))
v3.plot()
v3.print_eigenschappen()

v4 = Vorm(Lijn([0,0], [6,-3], [10,4]).gebruik_eenheid('cm'))
v4.plot()
v4.print_eigenschappen()


v5 = Vorm(Lijn([-50,-20], [50,-20], [50,20], [-50, 20]).transformeren(
          rotatiepunt=None, # bij None: neemt zwaartepunt
          rotatiehoek=20, # graden tegen de klok in
          schaalfactor=[1, -1], # vergroten om rotatiepunt; negatief:spiegelen
          translatie=[20, 20] # verplaatsing
    ).gebruik_eenheid('mm'))
v5.plot()
v5.print_eigenschappen()


v6 = Vorm(Lijn([2,0], [0,2], [8,10], [10, 8]).gebruik_eenheid('cm'))
v6.plot()
v6.print_eigenschappen()
h = float(Lijn((2,0), (0,2)))
b = float(Lijn((2,0), (10,8)))


if __name__ == '__main__':
    unittest.main()
