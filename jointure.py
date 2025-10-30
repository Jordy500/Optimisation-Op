import pandas as pd
import ast  # pour convertir le texte en dictionnaire Python

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




# Dictionnaires des prix et durées par mètre
prix_dict = {
    'aerien': 500,
    'semi-aerien': 750,
    'fourreau': 900
}

duree_dict = {
    'aerien': 2,
    'semi-aerien': 4,
    'fourreau': 5
}

def calculer_prix_et_duree(cluster_infra_str):
    try:
        # Convertir la chaîne en dictionnaire Python
        cluster = ast.literal_eval(cluster_infra_str)
        if not isinstance(cluster, dict):
            return pd.Series([0, 0])
        
        # Calcul du coût total et de la durée totale
        cout_total = 0
        duree_totale = 0
        for infra_type, longueur in cluster.items():
            prix_m = prix_dict.get(infra_type, 0)
            duree_h = duree_dict.get(infra_type, 0)
            cout_total += prix_m * longueur
            duree_totale += duree_h * longueur
        
        return pd.Series([cout_total, duree_totale])
    except Exception as e:
        print("Erreur sur :", cluster_infra_str)
        print(e)
        return pd.Series([0, 0])

# Appliquer la fonction pour chaque ligne
final_df[['cout_total', 'duree_totale']] = final_df['cluster_infra'].apply(calculer_prix_et_duree)

# Vérification du résultat
print(final_df.head())

# Sauvegarde
final_df.to_csv("all_for_one_avec_cout.csv", index=False)
print("✅ Fichier sauvegardé avec les colonnes cout_total et duree_totale")

