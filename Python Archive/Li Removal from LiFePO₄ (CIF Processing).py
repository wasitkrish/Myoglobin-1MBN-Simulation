from pymatgen.io.cif import CifParser
from pymatgen.transformations.standard_transformations import RemoveSpeciesTransformation

parser = CifParser("/home/krish/Desktop/Material-Informatics/Python/materials/LiFePO4.cif")
struct = parser.get_structures()[0]

t = RemoveSpeciesTransformation(["Li"])
new_struct = t.apply_transformation(struct)

new_struct.to(filename="/home/krish/Desktop/Material-Informatics/Python/export/delithiated_FePO4.cif") 
print("Saved to filename")