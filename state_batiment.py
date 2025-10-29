# definir les batiments qui ont de l'electricite et ceux qui non pas dans mon dataset reseau_en abre
import pandas as pd

network_data = pd.read_excel("reseau_en_arbre.xlsx")

# print(network_data['infra_type'].unique())

broken_network = network_data[network_data["infra_type"]=="a_remplacer"]

set_id_batiments = set(network_data["id_batiment"].values)
set_id_broken_batiments = set(broken_network["id_batiment"].values)

list_id_batiments, state_batiments = [], []

for id_batiment in set_id_batiments:
    list_id_batiments.append(id_batiment)
    if id_batiment in set_id_broken_batiments:
        state_batiments.append("a_reparer")  
    else:
        state_batiments.append("intact") 
        
        
state_df = pd.DataFrame({"id_batiment": list_id_batiments, "state_batiment": state_batiments})
state_df.columns = ["id_batiment", "state_batiment"]
state_df.to_excel("batiments_electricite.xlsx", index=False, columns=["id_batiment", "state_batiment"])

