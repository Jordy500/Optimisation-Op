import pandas as pd
# Jointure des différents fichiers de données
network_data = pd.read_excel("reseau_en_arbre.xlsx")
etat_network = pd.read_excel("etat_batiment.xlsx")
batiments = pd.read_csv("batiments.csv")
infras = pd.read_csv("infra.csv")

merged_batiment = pd.merge(network_data, etat_network, on='id_batiment')
merged_batiment.drop(columns=['nb_maisons'], inplace=True)
merged_batiment_number = pd.merge(merged_batiment, batiments, on='id_batiment')
final_df = pd.merge(merged_batiment_number, infras, left_on='infra_id', right_on='id_infra')

final_df.to_csv('all_for_one.csv', index=False)