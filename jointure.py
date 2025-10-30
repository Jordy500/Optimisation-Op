import pandas as pd

network_data = pd.read_csv("batiments_cluster_infra.csv")  # 85 lignes
etat_network = pd.read_excel("etat_batiment.xlsx")
batiments = pd.read_csv("batiments.csv")

# Supprimer les doublons dans etat_network et batiments
etat_network = etat_network.drop_duplicates(subset=['id_batiment'])
batiments = batiments.drop_duplicates(subset=['id_batiment'])

# Merge en gardant network_data comme base
merged_batiment = pd.merge(network_data, etat_network, on='id_batiment', how='left')
merged_batiment.drop(columns=['nb_maisons'], inplace=True)

final_df = pd.merge(merged_batiment, batiments, on='id_batiment', how='left')

print(len(final_df))  # devrait maintenant être 85

# Sauvegarder
final_df.to_csv('all_for_one.csv', index=False)
