from mp_api.client import MPRester
import pandas as pd

m=MPRester("Your API key")
fields=["material_id","formula_pretty","density"]
data = m.materials.search(
    formula=["SiO2","Al2O3","Fe2O3"],
    fields=fields
)
#conver results to a list of dictionaries
rows=[]

for mat in data:
    rows.append({
        "Material ID": mat.material_id,
        "Formula": mat.formula_pretty,
        "Density (g/cm3)": mat.density
    })
# Create Data Frame
df=pd.DataFrame(rows)
# Save to Excel
df.to_excel("export/material_data.xlsx",index=False)
print("Excel file printed successfully")