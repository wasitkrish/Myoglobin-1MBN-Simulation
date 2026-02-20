import pymatgen.core as pg 
fe=pg.Element("Fe")
print('atomic mass : ',fe.atomic_mass)
print('atomic number : ',fe.Z)
print('Melting point : ',fe.melting_point)

cmps = pg.Composition("NaCl")
print('weight composition : ',cmps.weight)
print('number of chlorine atoms in NaCl : ',cmps["Cl"])

ti=pg.Element("Ti")
print('atomic mass : ',ti.atomic_mass)
print('atomic number : ',ti.Z)
print('Melting point : ',ti.melting_point)