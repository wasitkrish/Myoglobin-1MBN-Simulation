from mp_api.client import MPRester
m=MPRester("yourapikey")
#initialize the MPRester with your API key
fields=[
    "material_id",
    "nsites",
    "density",
    "volume",
    "elements",
    "composition",
    "symmetry"
]
# Fetch material data using the search method and specifying fields
data_one = m.materials.search(material_ids=["mp-1010"],fields=fields)
#display the fetched data
print(data_one)
