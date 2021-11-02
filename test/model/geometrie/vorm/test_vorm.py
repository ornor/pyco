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


def print_props(obj):
    print('\n'.join(['{} = {}'.format(a, getattr(obj,a)) for a in obj.EIGENSCHAPPEN]))

l1 = Lijn(
        (4, -5), (-10, 10)
    ).lijn_cirkelboog(
        middelpunt=(0,0),
        gradenhoek=+220,
        stappen=100
    ).lijn_recht(
        naar=(4, 10)
    ).lijn_bezier(
        richting=(-10,-4),
        naar=(4, -5),
        stappen=20)

l2 = Lijn((0,0), (0,10), (4,10), (4,7), (6,7), (6,10), (10,10), (10,0))
l2.eenheid = 'cm'

v1 = Vorm(l1)
v1.plot()
v1.plot_net()
print()
print_props(v1)
print()

v2 = Vorm(l2, E=10000)
v2.plot()
v2.plot_net()
print()
print_props(v2)
print()

if __name__ == '__main__':
    unittest.main()
