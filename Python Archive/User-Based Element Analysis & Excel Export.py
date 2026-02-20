import pymatgen.core as pg 
import pandas as pd

n=int(input("\n Number of elements you want to process :"))

all_data = []

for i in range(n):
    element=str(input("Enter your element symbol : "))
    try:
        elm=pg.Element(element)
        comp=pg.Composition(element)
        print('atomic mass : ',elm.atomic_mass)
        print('atomic number : ',elm.Z)
        print('Melting point : ',elm.melting_point)
        print('Weight composition : ',comp.weight)
        print('\n')
        
        all_data.append({
            "Element": element,
            "Atomic mass": elm.atomic_mass,
            "Atomic number": elm.Z,
            "Melting point": elm.melting_point,
            "Weight Composition": comp.weight
        })
    except:
        print(f"Invalid element: {element}\n")

if all_data:
    df=pd.DataFrame(all_data)
    df.to_excel("/home/krish/Desktop/Material-Informatics/Python/export/user-based-element-analysis-and-export.xlsx", index=False)
    print("Data saved to user-based-element-analysis-and-export.xlsx")