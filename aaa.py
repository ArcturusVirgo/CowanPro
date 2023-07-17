from cowan.cowan.cowan import Atom

a = Atom(80, 2)
print(a.electron_arrangement)
a.arouse_electron('5d', '7s')
print(a.electron_arrangement)

print(a.get_configuration())
