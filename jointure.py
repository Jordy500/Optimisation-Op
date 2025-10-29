import pandas as pd
import numpy as np
# Jointure des différents fichiers de données
network_data = pd.read_excel("reseau_en_arbre.xlsx")
etat_network = pd.read_excel("etat_batiment.xlsx")
batiments = pd.read_csv("batiments.csv")
infras = pd.read_csv("infra.csv")

merged_batiment = pd.merge(network_data, etat_network, on='id_batiment')
merged_batiment.drop(columns=['nb_maisons'], inplace=True)
merged_batiment_number = pd.merge(merged_batiment, batiments, on='id_batiment')
final_df = pd.merge(merged_batiment_number, infras, left_on='infra_id', right_on='id_infra')

# Calcul des coûts et durées de réparation les mettre dans des tuples
def _rates(s):
    s = str(s).lower()
    if 'fourreau' in s:
        return 900.0, 5.0
    if 'semi' in s and ('aer' in s or 'aér' in s):
        return 750.0, 4.0
    #juste on sait jamais les ereurs de frappe
    if 'air' in s or 'aér' in s or 'aerien' in s or 'aérien' in s:
        return 500.0, 2.0
    if 'semi' in s:
        return 750.0, 4.0
    return np.nan, np.nan

type_col = 'type_infra'

# build per-meter rates
if type_col is not None:
    rates = final_df[type_col].astype(str).apply(_rates).tolist()
else:
    rates = [(np.nan, np.nan)] * len(final_df)
rates_df = pd.DataFrame(rates, columns=['prix_m', 'duree_h_m'])

length_col = 'longueur'

if length_col is not None:
    final_df['prix'] = rates_df['prix_m'] * final_df[length_col].astype(float)
    final_df['duree'] = rates_df['duree_h_m'] * final_df[length_col].astype(float)
else:
    # no length found: store per-meter rates instead just in case
    final_df['prix'] = rates_df['prix_m']
    final_df['duree'] = rates_df['duree_h_m']




final_df.to_csv('all_for_one.csv', index=False)