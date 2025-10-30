import pandas as pd

import ast
# Charger le fichier
network_data = pd.read_excel("reseau_en_arbre.xlsx")
df2 = pd.read_csv("infra.csv")

# Vérification des colonnes
required_cols = {'id_batiment', 'infra_id', 'infra_type', 'longueur'}
if not required_cols.issubset(network_data.columns):
    raise KeyError(f"Le fichier doit contenir les colonnes : {required_cols}")

# 🧹 Étape 1 : Supprimer toutes les lignes où infra_type contient 'intact'
cleaned_data = network_data[~network_data['infra_type'].str.lower().str.contains('intact', na=False)].copy()

print(f"✅ Lignes initiales : {len(network_data)}")
print(f"✅ Lignes après suppression des 'intact' : {len(cleaned_data)}")

# 🏗️ Étape 2 : Créer une colonne cluster_infra comme dictionnaire (infra_id: longueur)
def build_infra_dict(df):
    """Construit un dictionnaire {infra_id: longueur} pour un bâtiment donné."""
    return {infra: float(longueur) for infra, longueur in zip(df['infra_id'], df['longueur'])}

cluster_df = (
    cleaned_data
    .groupby('id_batiment')
    .apply(build_infra_dict)
    .reset_index(name='cluster_infra')
)

# 🧩 Étape 3 : Ajouter les autres colonnes (ex: nb_maisons, type, etc.)
# On prend la première valeur de chaque champ pour éviter la duplication
extra_cols = [
    col for col in cleaned_data.columns
    if col not in ['id_batiment', 'infra_id', 'longueur']
]

extra_info = (
    cleaned_data.groupby('id_batiment')[extra_cols].first().reset_index()
)

# Fusionner tout
final_df = pd.merge(extra_info, cluster_df, on='id_batiment', how='left')
print(final_df.head())


import pandas as pd
import ast

# Exemple : df2 contient la correspondance id_infra → type_infra
# df2 = pd.read_csv("infra_types.csv")
infra_map = dict(zip(df2['id_infra'], df2['type_infra']))

def add_type_to_infra(cluster_str):
    if pd.isna(cluster_str):
        return None
    try:
        # Convertir la chaîne en dictionnaire
        if isinstance(cluster_str, str):
            cluster_dict = ast.literal_eval(cluster_str)
        else:
            cluster_dict = cluster_str

        new_dict = {}
        for infra_id, longueur in cluster_dict.items():
            # On crée une clé tuple : (infra_id, type_infra)
            type_infra = infra_map.get(infra_id, "inconnu")
            new_dict[(infra_id, type_infra)] = longueur

        return new_dict

    except Exception as e:
        print("Erreur sur :", cluster_str)
        print(e)
        return None



# Appliquer la fonction
final_df['cluster_infra'] = final_df['cluster_infra'].apply(add_type_to_infra)

# Vérifier
print(final_df.head())

# Sauvegarder
final_df.to_csv('batiments_cluster_infra.csv', index=False)