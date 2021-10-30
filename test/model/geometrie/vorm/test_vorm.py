import unittest

from pyco.interface import Document

doc = Document()
fn = doc.functies
Waarde = doc.model.Waarde
Knoop = doc.model.Knoop
Lijn = doc.model.Lijn
Vorm = doc.model.Vorm

class TestVorm(unittest.TestCase):

    def test_Vorm(self):
        self.assertRaises(TypeError, lambda: Lijn('str', 'str'))
        assert Lijn(Knoop(1, 2), Knoop(3, 4)) == Lijn([Knoop(1, 2), Knoop(3, 4)])



l1 = Lijn(
        (4, -5), (-10, 10)
    ).lijn_cirkelboog(
        middelpunt=(0,0),
        gradenhoek=+220,
        stappen=50
    ).lijn_recht(
        naar=(4, 10)
    ).lijn_bezier(
        richting=(-10,-4),
        naar=(4, -5),
        stappen=50)

l2 = Lijn((0,0), (10,0), (10,10), (0,10))
l2.eenheid = 'cm'

v1 = Vorm(l1)
#print(v1.array)
v1.plot()
print('A =', repr(v1.A_))
print('z =', repr(v1.z_))
print('O =', repr(v1.O_))
print()

v2 = Vorm(l2)
#print(v2.array)
v2.plot()
print('A =', repr(v2.A_))
print('z =', repr(v2.z_))
print('O =', repr(v2.O_))
print()




if __name__ == '__main__':
    unittest.main()
