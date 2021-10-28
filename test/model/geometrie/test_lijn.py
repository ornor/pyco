import unittest

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde
Knoop = doc.model.Knoop
Lijn = doc.model.Lijn

class TestLijn(unittest.TestCase):

    def test_Lijn(self):
        self.assertRaises(TypeError, lambda: Lijn('str', 'str'))
        self.assertRaises(ValueError, lambda: Lijn(Knoop(1, 2)))
        self.assertRaises(ValueError, lambda: Lijn(Knoop(1, 2), Knoop(Waarde(1).cm, Waarde(2).cm)))
        assert Lijn(Knoop(1, 2), Knoop(3, 4)) == Lijn([Knoop(1, 2), Knoop(3, 4)])
        assert Lijn((1, 2), (1, 2), (3, 4), (3, 4), (3, 4)) == Lijn(Knoop(1, 2), Knoop(3, 4))

    def test_eenheid(self):
        l1 = Lijn((1, 2), (3, 4))
        l1.eenheid = 'mm'
        assert str(l1) == '((1.0, 2.0), (3.0, 4.0)) mm'
        l2 = Lijn(Knoop(Waarde(1).cm, Waarde(2).cm), Knoop(Waarde(3).cm, Waarde(4).cm))
        l2.eenheid = 'mm'
        assert str(l2) == '((10.0, 20.0), (30.0, 40.0)) mm'

    def test___eq__(self):
        l1 = Lijn(Knoop(Waarde(1).cm, Waarde(2).cm), Knoop(Waarde(3).cm, Waarde(4).cm))
        l2 = Lijn((Waarde(10).mm, Waarde(20).mm), (Waarde(.3).dm, Waarde(.4).dm))
        assert l1 == l2

    def test___neq__(self):
        l1 = Lijn(Knoop(Waarde(1).cm, Waarde(2).cm), Knoop(Waarde(3).cm, Waarde(4).cm))
        l2 = Lijn(Knoop(1, 2), Knoop(3, 4))
        assert l1 != l2

    def test___iter__(self):
        assert tuple(Lijn(Knoop(1,2), Knoop(3,4))) == (Knoop(1,2), Knoop(3,4))

    def test___getitem__(self):
        assert Lijn(Knoop(1,2), Knoop(3,4))[1] == Knoop(3,4)

    def test___len__(self):
        assert len(Lijn(Knoop(1,2), Knoop(3,4))) == 2

    def test___format__(self):
        assert format(Lijn((1, 2), (3, 4)), '.3f') == '((1.000, 2.000), (3.000, 4.000))'
        assert format(Lijn((Waarde(10).mm, Waarde(20).mm), (Waarde(.3).dm, Waarde(.4).dm)), '.1e') == '((1.0e+01, 2.0e+01), (3.0e+01, 4.0e+01)) mm'

    def test___repr__(self):
        assert repr(Lijn((1, 2), (3, 4))) == 'Lijn(Knoop(1.0, 2.0), Knoop(3.0, 4.0))'
        assert repr(Lijn(Knoop(Waarde(1).cm, Waarde(2).cm), Knoop(Waarde(3).cm, Waarde(4).cm))) == "Lijn(Knoop(Waarde(1.0, 'cm'), Waarde(2.0, 'cm')), Knoop(Waarde(3.0, 'cm'), Waarde(4.0, 'cm')))"

    def test___str__(self):
        assert str(Lijn((1, 2), (3, 4))) == '((1.0, 2.0), (3.0, 4.0))'
        assert str(Lijn(Knoop(Waarde(1).cm, Waarde(2).cm), Knoop(Waarde(3).cm, Waarde(4).cm))) == '((1.0, 2.0), (3.0, 4.0)) cm'


if __name__ == '__main__':
    unittest.main()
