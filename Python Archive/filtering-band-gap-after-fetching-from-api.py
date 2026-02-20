from mp_api.client import MPRester
import pandas as pd

API_KEY="your api key"

with MPRester(API_KEY) as m:
    data = m.summary.search(
        formula="SiO2",
        fields=["material_id","formula_pretty","band_gap"]
    )
    
    filtered_data=[
        mat for mat in data
        if mat.band_gap is not None and mat.band_gap > 5
    ]

rows=[]
for mat in filtered_data:
    rows.append({
        "Material ID": mat.material_id,
        "Formula": mat.formula_pretty,
        "Band Gap (eV)": mat.band_gap
    })
df=pd.DataFrame(rows)
df.to_excel("export/filtered_band_gap.xlsx",index=False)
print("Data written successfully")
    
    