import shelve
from Cowan.cowan.cowan import Atom
a = Atom(1, 0)
obj_info = shelve.open('F:/Cowan/Cl/.cowan/obj_info')

a= obj_info['atom']
print(list(obj_info.keys()))

