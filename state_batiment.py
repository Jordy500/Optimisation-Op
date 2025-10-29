# definir les batiments qui ont de l'electricite et ceux qui non pas dans mon dataset reseau_en abre

import pandas as pd

network_data = pd.read_excel("reseau_en_arbre.xlsx")

print(network_data.head())

broken_network = network_data[network_data['infra_id'] == 'en panne']

set_id_batiments_sans_electricite = set(broken_network['set_id'].values)
set_id_broken_batiments = set(broken_network['set_id_batiment'].values)

list_id_batiments, state_batiments = [], []

for id_batiment in network_data['set_id_batiment'].values:
    list_id_batiments.append(id_batiment)
    if id_batiment in set_id_broken_batiments:
        state_batiments.append(0)  # 0 signifie pas d'electricite
    else:
        state_batiments.append(1)  # 1 signifie avec electricite
        
        
state_df = pd.DataFrame({'set_id_batiment': list_id_batiments, 'state_batiment': state_batiments})
state_df.to_csv('batiments_electricite.csv', index=False)
state_df.to_excel('batiments_electricite.xlsx', index=False, columns=['set_id_batiment', 'state_batiment'])