import unittest

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde
Knoop = doc.model.Knoop

class TestKnoop(unittest.TestCase):

    def test_Knoop(self):
        self.assertRaises(TypeError, lambda: Knoop('str'))
        self.assertRaises(TypeError, lambda: Knoop(4, Waarde('str')))
        assert Knoop(4, 5, 6).eenheid == None
        assert Knoop(Waarde(4), 5, 6).eenheid == None
        assert Knoop(Waarde(4).cm, Waarde(4, 'mm')).eenheid == 'cm'
        assert tuple(Knoop(Waarde(5, 'cm'), Waarde(6, 'm'))) ==  (5.0, 600.0)
        self.assertRaises(TypeError, lambda: Knoop(Waarde(5, 'cm'), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Knoop(Waarde(5), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Knoop(5, Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Knoop(Waarde(6, 's'), 5))
        self.assertRaises(ValueError, lambda: Knoop())
        assert Knoop(4, 5, 6) == Knoop([4, 5, 6])
        self.assertRaises(ValueError, lambda: Knoop(Waarde(6, 's'), Waarde(6, 's')))

    def test___add__(self):
        assert Knoop(3, 4) + Knoop(6, 7) == Knoop(9, 11)

    def test_x(self):
        assert Knoop(3, 4, 5).x == 3.0
        assert Knoop(Waarde(2, 'cm'), Waarde(30, 'mm')).x == Waarde(2, 'cm')

    def test_y(self):
        self.assertRaises(IndexError, lambda: Knoop(5).y)
        assert Knoop(3, 4, 5).y == 4.0
        assert Knoop(Waarde(2, 'cm'), Waarde(30, 'mm')).y == Waarde(3, 'cm')

    def test_z(self):
        self.assertRaises(IndexError, lambda: Knoop(5, 6).z)
        assert Knoop(3, 4, 5).z == 5.0
        assert Knoop(Waarde(2, 'cm'), Waarde(30, 'mm'), Waarde(0.4, 'dm')).z == Waarde(4, 'cm')

    def test___format__(self):
        assert format(Knoop(Waarde(34, 'cm')), '.3f') == '(34.000) cm'

    def test___repr__(self):
        assert repr(Knoop(3, 4, 5)) == 'Knoop(3.0, 4.0, 5.0)'

    def test___str__(self):
        assert str(Knoop(3, 4)) == '(3.0, 4.0)'


if __name__ == '__main__':
    unittest.main()
