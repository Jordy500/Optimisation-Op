# definir les batiments qui ont de l'electricite et ceux qui non pas dans mon dataset reseau_en abre

import pandas as pd

network_data = pd.read_excel("reseau_en_arbre.xlsx")
broken_network = network_data[network_data['infra_type'] == 'a_remplacer']

set_id_batiments  = set(network_data['id_batiment'].values)
set_id_broken_batiments = set(broken_network['id_batiment'].values)

list_id_batiments, state_batiment = [], []

for id_batiment in network_data['id_batiment'].values:
    list_id_batiments.append(id_batiment)
    if id_batiment in set_id_broken_batiments:
        state_batiment.append("a_reparer")  # 0 signifie pas d'electricite
    else:
        state_batiment.append("intact")  # 1 signifie avec electricite
        
        
state_df = pd.DataFrame({'id_batiment': list_id_batiments, 'state_batiment': state_batiment})
state_df.columns = ['id_batiment', 'state_batiment']
state_df.to_excel('etat_batiment.xlsx', index=False)