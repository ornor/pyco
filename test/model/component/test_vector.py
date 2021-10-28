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
        assert Vector(4, 5, 6).eenheid == None
        assert Vector(Waarde(4), 5, 6).eenheid == None
        assert Vector(Waarde(4).cm, Waarde(4, 'mm')).eenheid == 'cm'
        assert tuple(Vector(Waarde(5, 'cm'), Waarde(6, 'm'))) ==  (5.0, 600.0)
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'cm'), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5), Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(5, Waarde(6, 's')))
        self.assertRaises(TypeError, lambda: Vector(Waarde(6, 's'), 5))
        self.assertRaises(ValueError, lambda: Vector())
        assert Vector(4, 5, 6) == Vector([4, 5, 6])

    def test_eenheid(self):
        assert Vector(3, 4, 5).eenheid is None
        assert Vector(Waarde(4), Waarde(5)).eenheid is None
        assert Vector(Waarde(4).cm, Waarde(4, 'mm')).eenheid == 'cm'
        v = Vector(3, 4, 5)
        v.eenheid = 'm'
        assert str(v) == '(3.0, 4.0, 5.0) m'
        v = Vector(Waarde(5, 'cm'), Waarde(6, 'm'))
        v.eenheid = 'dm'
        assert str(v) == '(0.5, 60.0) dm'

    def test___add__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) + 4)
        assert Vector(3, 4) + Vector(5, 6) == Vector(8, 10)
        assert Vector(Waarde(3, 'm')) + Vector(Waarde(5, 'cm')) == Vector(Waarde(30.5, 'dm'))
        self.assertRaises(TypeError, lambda: Vector(Waarde(3, 'm')) + Vector(Waarde(5, 's')))
        assert Vector(3, 4) + Vector(5, 6, 1) == Vector(8, 10, 1)

    def test___sub__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) - 4)
        assert Vector(3, 4) - Vector(5, 6) == Vector(-2, -2)
        assert Vector(Waarde(3, 'm')) - Vector(Waarde(5, 'cm')) == Vector(Waarde(29.5, 'dm'))
        self.assertRaises(TypeError, lambda: Vector(Waarde(3, 'm')) - Vector(Waarde(5, 's')))
        assert Vector(3, 4) - Vector(5, 6, 1) == Vector(-2, -2, -1)

    def test___mul__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) * 'str')
        assert Vector(3, 4) * Vector(5, 6) == 39.0
        assert Vector(Waarde(30, 'mm')) * Vector(Waarde(5, 'cm')) == Waarde(15, 'cm2')
        assert Vector(Waarde(30, 'mm'), Waarde(30, 'mm')) * Vector(Waarde(5, 'cm'), Waarde(5, 'cm')) == Waarde(30, 'cm2')
        assert Vector(3, 4) * Vector(5, 6, 10) == 39.0
        assert Vector(3, 4) * 6 == Vector(18, 24)
        assert Vector(Waarde(3, 'cm'), Waarde(40, 'mm')) * -0.5 == Vector(Waarde(-1.5, 'cm'), Waarde(-2, 'cm'))

    def test___truediv__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) / 'str')
        assert Vector(3, 6) / Vector(6, 6) == 1.5
        assert Vector(Waarde(30, 'mm')) / Vector(Waarde(6, 'cm')) == Waarde(0.5)
        assert Vector(Waarde(30, 'mm'), Waarde(30, 'mm')) / Vector(Waarde(5, 'cm'), Waarde(5, 'cm')) == Waarde(1.2)
        assert Vector(3, 4) / Vector(5, 6, 10) == 3.8/3
        assert Vector(3, 4) / 6 == Vector(0.5, 2/3)
        assert Vector(Waarde(3, 'cm'), Waarde(40, 'mm')) / -0.5 == Vector(Waarde(-6, 'cm'), Waarde(-8, 'cm'))

    def test___pow__(self):
        self.assertRaises(ValueError, lambda: Vector(5, 6) ** -1)
        self.assertRaises(ValueError, lambda: Vector(5, 6) ** 1)
        self.assertRaises(ValueError, lambda: Vector(5, 6) ** 'str')
        assert Vector(5, 6) ** 2 == 61.0
        assert Vector(5, 6) ** 3 == 3721.0
        assert Vector(Waarde(30, 'mm'), Waarde(5, 'cm')) ** 2 == Waarde(0.0034, 'm2')
        assert Vector(Waarde(30, 'mm'), Waarde(5, 'cm')) ** 3 == Waarde(0.00001156, 'm4')

    def test___rmul__(self):
        self.assertRaises(TypeError, lambda: 'str' * Vector(5, 6))
        assert 6 * Vector(3, 4) == Vector(18, 24)
        assert -0.5 * Vector(Waarde(3, 'cm'), Waarde(40, 'mm')) == Vector(Waarde(-1.5, 'cm'), Waarde(-2, 'cm'))

    def test___rtruediv__(self):
        self.assertRaises(TypeError, lambda: 'str' / Vector(5, 6))
        assert 6 / Vector(3, 4) == Vector(2.0, 1.5)

    def test___eq__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) == 4)
        assert Vector(4, 5, 6) == Vector(4.0, 5.0, 6.0)
        v = Vector(4, 5)
        v.eenheid = 'mm'
        assert v == Vector(Waarde(4, 'mm'), Waarde(0.5, 'cm'))
        assert not Vector(4) == Vector(4, 5)
        assert not Vector(4) == Vector(Waarde(4, 'mm'))
        assert not Vector(Waarde(4, 'mm')) == Vector(4)
        assert not Vector(Waarde(4, 'mm')) == Vector(Waarde(4, 's'))
        assert Vector(Waarde(500.0, 'cm'), Waarde(600.0, 'cm')) == Vector(Waarde(5.0, 'm'), Waarde(6.0, 'm'))

    def test___neq__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) != 4)
        assert not Vector(4, 5, 6) != Vector(4.0, 5.0, 6.0)
        v = Vector(4, 5)
        v.eenheid = 'mm'
        assert not v != Vector(Waarde(4, 'mm'), Waarde(0.5, 'cm'))
        assert Vector(4) != Vector(4, 5)
        assert Vector(4) != Vector(Waarde(4, 'mm'))
        assert Vector(Waarde(4, 'mm')) != Vector(4)
        assert Vector(Waarde(4, 'mm')) != Vector(Waarde(4, 's'))

    def test___lt__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) < 4)
        self.assertRaises(TypeError, lambda: Vector(5, 6) < Vector(4))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'm')) < Vector(Waarde(5, 's')))
        assert Vector(Waarde(40, 'mm')) < Vector(Waarde(5, 'cm'))
        assert Vector(Waarde(30, 'mm'), Waarde(30, 'mm')) < Vector(Waarde(30, 'mm'), Waarde(40, 'mm'))

    def test___gt__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) > 4)
        self.assertRaises(TypeError, lambda: Vector(5, 6) > Vector(4))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'm')) > Vector(Waarde(5, 's')))
        assert Vector(Waarde(60, 'mm')) > Vector(Waarde(5, 'cm'))
        assert Vector(Waarde(30, 'mm'), Waarde(40, 'mm')) > Vector(Waarde(30, 'mm'), Waarde(30, 'mm'))

    def test___le__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) <= 4)
        self.assertRaises(TypeError, lambda: Vector(5, 6) <=  Vector(4))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'm')) <=  Vector(Waarde(5, 's')))
        assert Vector(Waarde(40, 'mm')) <= Vector(Waarde(5, 'cm'))
        assert Vector(Waarde(30, 'mm'), Waarde(30, 'mm')) <= Vector(Waarde(30, 'mm'), Waarde(40, 'mm'))
        assert Vector(Waarde(40, 'mm')) <= Vector(Waarde(4, 'cm'))

    def test___ge__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) >= 4)
        self.assertRaises(TypeError, lambda: Vector(5, 6) >= Vector(4))
        self.assertRaises(TypeError, lambda: Vector(Waarde(5, 'm')) >= Vector(Waarde(5, 's')))
        assert Vector(Waarde(60, 'mm')) >= Vector(Waarde(5, 'cm'))
        assert Vector(Waarde(30, 'mm'), Waarde(40, 'mm')) >= Vector(Waarde(30, 'mm'), Waarde(30, 'mm'))
        assert Vector(Waarde(40, 'mm')) >= Vector(Waarde(4, 'cm'))

    def test___and__(self):
        self.assertRaises(TypeError, lambda: Vector(5, 6) & 4)
        assert Vector(Waarde(1, 'mm')) & Vector(Waarde(1, 'cm'))
        assert not Vector(Waarde(1, 'mm')) & Vector(Waarde(1, 's'))

    def test___float__(self):
        assert float(Vector(3, 4)) == 5.0
        assert float(Vector(Waarde(3, 'cm'), Waarde(40, 'mm'))) == 5.0

    def test___abs__(self):
        assert abs(Vector(3, 4)) == Waarde(5)
        assert abs(Vector(Waarde(3, 'cm'), Waarde(40, 'mm'))) == Waarde(0.5, 'dm')

    def test___pos__(self):
        assert Vector(3, -4) == +Vector(3, -4)

    def test___neg__(self):
        assert Vector(-3, 4) == -Vector(3, -4)

    def test___bool__(self):
        assert bool(Vector(1, 1)) == True
        assert bool(Vector(0, 0)) == False

    def test___iter__(self):
        assert tuple(Vector(3)) == (3.0,)
        assert tuple(Vector(3, 4)) == (3.0, 4.0)
        assert tuple(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == (Waarde(3, 'm'), Waarde(0.05, 'm'))

    def test___len__(self):
        assert len(Vector(3)) == 1
        assert len(Vector(3, 4)) == 2

    def test___format__(self):
        assert format(Vector(3, 4, 5)) == '(3.0, 4.0, 5.0)'
        assert format(Vector(3, 4, 5), '.0f') == '(3, 4, 5)'
        assert format(Vector(Waarde(34, 'cm')), '.3f') == '(34.000) cm'
        assert format(Vector(Waarde(340, 'cm').m), '.3f') == '(3.400) m'
        assert format(Vector(Waarde(34000, 'cm').m), '.1e') == '(3.4e+02) m'
        assert format(Vector(Waarde(12, 'cm'), Waarde(34, 'mm')), '.3f') == '(12.000, 3.400) cm'

    def test___repr__(self):
        assert repr(Vector(3, 4, 5)) == 'Vector(3.0, 4.0, 5.0)'
        assert repr(Vector([3, 4, 5])) == 'Vector(3.0, 4.0, 5.0)'
        assert repr(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == "Vector(Waarde(3.0, 'm'), Waarde(0.05, 'm'))"

    def test___str__(self):
        assert str(Vector(3, 4)) == '(3.0, 4.0)'
        assert str(Vector(Waarde(3, 'm'), Waarde(5, 'cm'))) == '(3.0, 0.05) m'

    def test___getitem__(self):
        assert Vector(3)[0] == 3.0
        assert Vector(3, 4)[1] == 4.0
        assert Vector(Waarde(3, 'm'), Waarde(5, 'cm'))[1] == Waarde(0.05, 'm')
        assert Vector(3, 4, 5, 6)[2:] == Vector(5, 6)
        assert Vector(3, 4, 5)[:] == Vector(3, 4, 5)
        v = Vector(3, 4, 5, 6)
        v.eenheid = 'm'
        assert v[2:] == Vector(Waarde(5).m, Waarde(6).m)


if __name__ == '__main__':
    unittest.main()
