import pymatgen.core as pg 
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
 
lattice = pg.Lattice.cubic(4.2)
print('LATTICE\n',lattice,"\n")
structure = pg.Structure(lattice, ["Li","Cl"], [[0,0,0],[0.5,0.5,0.5]])
print('STRUCTURE','\n',structure)
structure.to(fmt="poscar")
structure.to(filename="/home/krish/Desktop/Material-Informatics/Python/export/POSCAR")
structure.to(filename="/home/krish/Desktop/Material-Informatics/Python/export/CsCl.cif")
