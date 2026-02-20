import pymatgen.core as pg 
import pandas as pd

inputpath="/home/krish/Desktop/Material-Informatics/Python/materials/molecularformula.xlsx"

try:
    df_in = pd.read_excel(inputpath,engine="openpyxl")
except Exception as exc:
    raise SystemExit(f"Failed to read XLSX : {exc}")

if df_in.shape[1]<2:
    raise SystemExit("Input files must have at least two columns")

elements = df_in.iloc[:,1].dropna().astype(str).tolist()
all_data=[]

for element in elements:
    element=element.strip()
    if not element:
        continue
    try:
        elm=pg.Element(element)
        comp=pg.Composition(element)
        print("Atomic mass : ",elm.atomic_mass)
        print("Atomic Number : ",elm.Z)
        print("Melting point : ",elm.melting_point)
        print("Weight composition",comp.weight)
        print("\n")
        
        all_data.append({
            "Element": element,
            "Atomic mass": elm.atomic_mass,
            "Atomic number": elm.Z,
            "Melting point": elm.melting_point,
            "Weight composition": comp.weight
        })
    except Exception:
        print(f"invalid element: {element}\n")
        
    if all_data:
        df_out=pd.DataFrame(all_data)
        df_out.to_excel("/home/krish/Desktop/Material-Informatics/Python/export/element-property-from-excel-input.xlsx",index=False)
        print("Data saved to element-property-from-excel-input.xlsx")
    else:
        print("No valid element found")