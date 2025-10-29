# definir les batiments qui ont de l'electricite et ceux qui non pas dans mon dataset reseau_en abre

import pandas as pd

network_data = pd.read_excel("reseau_en_arbre.xlsx")

print(network_data.head())

broken_network = network_data[network_data['infra_id'] == 'en panne']

set_id_batiments_sans_electricite = set(broken_network['id_batiment'].values)
set_id_broken_batiments = set(broken_network['id_batiment'].values)

list_id_batiments, state_batiments = [], []

for id_batiment in network_data['id_batiment'].values:
    list_id_batiments.append(id_batiment)
    if id_batiment in set_id_broken_batiments:
        state_batiments.append("en panne")  # 0 signifie pas d'electricite
    else:
        state_batiments.append("intact")  # 1 signifie avec electricite
        
        
state_df = pd.DataFrame({'id_batiment': list_id_batiments, 'state_batiment': state_batiments})
state_df.columns = ['id_batiment', 'state_batiment']
state_df.to_excel('batiments_electricite.xlsx', index=False, columns=['id_batiment', 'state_batiment'])