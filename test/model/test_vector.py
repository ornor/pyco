import unittest

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde
Vector = doc.model.Vector


class TestVector(unittest.TestCase):

    def test_Vector(self):
        self.assertRaises(TypeError, lambda: Vector('str'))
        self.assertRaises(TypeError, lambda: Vector(4, Waarde('str')))
        assert Vector(4, 5, 6)._eenheid == None
        assert Vector(Waarde(4), 5, 6)._eenheid == None
        assert Vector(Waarde(4).cm, Waarde(4, 'mm')).eenheid == 'cm'
        assert tuple(Vector(Waarde(5, 'cm'), Waarde(6, 'm'))) ==  (5.0, 600.0)
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'cm'), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(5, Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(Waarde(6, 's'), 5))

    def test_eenheid(self):
        assert Vector(3, 4, 5).eenheid is None
        assert Vector(Waarde(4).cm, Waarde(4, 'mm')).eenheid == 'cm'

    def test___add__(self):
        pass

    def test___sub__(self):
        pass

    def test___mul__(self):
        pass

    def test___truediv__(self):
        pass

    def test___pow__(self):
        pass

    def test___rmul__(self):
        pass

    def test___rtruediv__(self):
        pass

    def test___eq__(self):
        pass

    def test___neq__(self):
        pass

    def test___lt__(self):
        pass

    def test___gt__(self):
        pass

    def test___le__(self):
        pass

    def test___ge__(self):
        pass

    def test___and__(self):
        pass

    def test___float__(self):
        pass

    def test___abs__(self):
        pass

    def test___pos__(self):
        pass

    def test___neg__(self):
        pass

    def test___bool__(self):
        pass

    def test___iter__(self):
        assert tuple(Vector(3)) == (3.0,)
        assert tuple(Vector(3, 4)) == (3.0, 4.0)
        assert tuple(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == (3.0, 0.05)

    def test___len__(self):
        pass

    def test___format__(self):
        pass

    def test___repr__(self):
        assert repr(Vector(3, 4, 5)) == 'Vector(3.0, 4.0, 5.0)'
        assert repr(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == "Vector(Waarde(3.0, 'm'), Waarde(0.05, 'm'))"

    def test___str__(self):
        assert str(Vector(3, 4)) == '[3.0, 4.0]'
        assert str(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == '[3.0, 0.05] m'

    def test___getitem__(self):
        pass

if __name__ == '__main__':
    unittest.main()
