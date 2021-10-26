import unittest

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde


class TestWaarde(unittest.TestCase):

    def test_Waarde(self):
        assert Waarde(120, 'mm') == Waarde(120).mm
        assert Waarde(1, 'Pa') == Waarde(1, 'N/m2')
        assert Waarde(2*fn.pi, 'rad') == Waarde(360, 'deg')
        assert Waarde(0, 'K') == Waarde(-273.15, 'C')
        assert Waarde(40, 'C') == Waarde(104, 'F')
        assert Waarde(6, 'K') == Waarde(-448.87, 'F')
        assert Waarde(1, 's*m/m4') == Waarde(1, 's/m3')

    def test___add__(self):
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') + 2)
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') + Waarde('str'))
        self.assertRaises(TypeError, lambda: Waarde('str') + Waarde(1, 'mm'))
        self.assertRaises(TypeError, lambda: Waarde(1, 's') + Waarde(1, 'mm'))
        assert Waarde(120, 'mm') + Waarde(30, 'cm') == Waarde(0.42, 'm')

    def test___sub__(self):
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') - 2)
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') - Waarde('str'))
        self.assertRaises(TypeError, lambda: Waarde('str') - Waarde(1, 'mm'))
        self.assertRaises(TypeError, lambda: Waarde(1, 's') - Waarde(1, 'mm'))
        assert Waarde(520, 'mm') - Waarde(30, 'cm') == Waarde(0.22, 'm')

    def test___mul__(self):
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') * 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') * Waarde('str'))
        self.assertRaises(TypeError, lambda: Waarde('str') * Waarde(1, 'mm'))
        assert Waarde(3, 'm') * Waarde(4, 's') == Waarde(12.0, 'm*s')
        assert Waarde(3, 'm') * 6 == Waarde(18.0, 'm')

    def test___truediv__(self):
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') / 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') / Waarde('str'))
        self.assertRaises(TypeError, lambda: Waarde('str') / Waarde(1, 'mm'))
        assert Waarde(20, 'ha') / Waarde(5, 'km') == Waarde(40.0, 'm')
        assert Waarde(3, 'm') / 4 == Waarde(0.75, 'm')

    def test___pow__(self):
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') ** 3.1)
        self.assertRaises(TypeError, lambda: Waarde('str') ** 3)
        assert Waarde(2, 'm') ** 3 == Waarde(8.0, 'm3')

    def test___rmul__(self):
        self.assertRaises(TypeError, lambda: 'str' * Waarde(1, 'mm'))
        self.assertRaises(TypeError, lambda: 3 * Waarde('str'))
        assert 2 * Waarde(4, 's') == Waarde(8.0, 's')

    def test___rtruediv__(self):
        self.assertRaises(TypeError, lambda: 'str' / Waarde(1, 'mm'))
        self.assertRaises(TypeError, lambda: 3 / Waarde('str'))
        assert 2 / Waarde(4, 's') == Waarde(0.5, '1/s')

    def test___eq__(self):
        assert Waarde(42, 'mm') == 42
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') == 'str')
        assert not Waarde(1, 'mm') == Waarde(1, 's')
        assert Waarde(3).cm == Waarde(30).mm
        assert Waarde(3.0000000000001).cm == Waarde(30).mm

    def test___neq__(self):
        assert not Waarde(42, 'mm') != 42
        assert Waarde(42, 'mm') != 3
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') != 'str')
        assert Waarde(1, 'mm') != Waarde(1, 's')
        assert Waarde(3).cm != Waarde(4).cm

    def test___lt__(self):
        assert Waarde(42, 'mm') < 50
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') < 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') < Waarde(1, 's'))
        assert Waarde(2).cm < Waarde(30).mm

    def test___gt__(self):
        assert Waarde(42, 'mm') > 30
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') > 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') > Waarde(1, 's'))
        assert Waarde(4).cm > Waarde(30).mm

    def test___le__(self):
        assert Waarde(42, 'mm') <= 50
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') <= 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') <= Waarde(1, 's'))
        assert Waarde(2).cm <= Waarde(30).mm
        assert Waarde(2).cm == Waarde(20).mm

    def test___ge__(self):
        assert Waarde(42, 'mm') >= 30
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') >= 'str')
        self.assertRaises(TypeError, lambda: Waarde(1, 'mm') >= Waarde(1, 's'))
        assert Waarde(2.9999999999999).cm >= Waarde(30).mm
        assert Waarde(4).cm >= Waarde(30).mm

    def test___and__(self):
        assert Waarde(4, 'mm') & Waarde(5, 'm2/km')
        assert Waarde(5) & Waarde(7)
        assert Waarde('foo') & Waarde('str')
        assert not Waarde(4) & Waarde('str')
        assert not Waarde(4, 'm') & Waarde(5, 's')

    def test___float__(self):
        assert float(Waarde(30, 'mm').cm) == 3.0
        assert float(Waarde(30).mm.cm) == float(Waarde(3))

    def test___abs__(self):
        assert abs(Waarde(-4)) == Waarde(4)
        assert abs(Waarde(4)) == Waarde(4)
        assert abs(Waarde('foo')) == Waarde('foo')

    def test___pos__(self):
        assert Waarde(4) == +Waarde(4)
        assert Waarde('str') == +Waarde('str')

    def test___neg__(self):
        assert Waarde(-4) == -Waarde(4)
        assert Waarde(4) == -Waarde(-4)
        assert Waarde('str') == -Waarde('str')

    def test___bool__(self):
        assert bool(Waarde(0)) is False
        assert bool(Waarde(4)) is True
        assert bool(Waarde('foo')) is True
        assert bool(Waarde('')) is False

    def test___iter__(self):
        assert (34.0, 'cm') == tuple(Waarde(34, 'cm'))
        assert (34.0, '') == tuple(Waarde(34))
        assert ('str', '') == tuple(Waarde('str'))

    def test___len__(self):
        assert len(Waarde(34, 'cm')) == 2

    def test___format__(self):
        assert format(Waarde(34, 'cm'), '.3f') == '34.000 cm'
        assert format(Waarde(340, 'cm').m, '.3f') == '3.400 m'
        assert format(Waarde(34000, 'cm').m, '.1e') == '3.4e+02 m'
        assert format(Waarde('str'), '.2') == 'st'
        assert format(Waarde('str'), '>10') == '       str'
        assert format(Waarde('str'), '<10') == 'str       '
        assert format(Waarde('str'), '^10') == '   str    '
        assert format(Waarde('str'), '-^10') == '---str----'

    def test___repr__(self):
        assert repr(Waarde(34)) == "Waarde(34.0)"
        assert repr(Waarde(34).cm) == "Waarde(34.0, 'cm')"
        assert repr(Waarde('str')) == "Waarde('str')"

    def test___str__(self):
        assert str(Waarde(3).cm) == '3.00 cm'
        assert str(Waarde(3).cm._4) == '3.0000 cm'
        assert str(Waarde('Foo')) == 'Foo'

    def test___getitem__(self):
        assert Waarde(3, 'm') == Waarde(300)['cm']['m']
        assert str(Waarde(3)[12]) == '3.000000000000'


if __name__ == '__main__':
    unittest.main()
