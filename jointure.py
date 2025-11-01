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

print(final_df)  # devrait maintenant être 85


import ast
import pandas as pd

def calculer_prix_et_duree(cluster_infra_str):
    WORKERS = 4
    HOURLY_RATE = 300 / 8  # 37.5 €/h

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

    try:
        # Conversion chaîne → dictionnaire
        if isinstance(cluster_infra_str, str):
            cluster = ast.literal_eval(cluster_infra_str)
        else:
            cluster = cluster_infra_str

        if not isinstance(cluster, dict):
            return pd.Series([0, 0, 0, 0])

        cout_materiel = 0.0
        cout_main_oeuvre = 0.0
        durees_effectives = []  # Pour stocker les durées parallèles

        for key, longueur in cluster.items():
            if isinstance(key, tuple):
                _, infra_type = key
            else:
                infra_type = key

            prix_m = prix_dict.get(infra_type)
            duree_h = duree_dict.get(infra_type)

            if prix_m is None or duree_h is None:
                print(f" Type inconnu : {infra_type}")
                continue

            try:
                longueur = float(longueur)
            except ValueError:
                print(f" Longueur invalide : {longueur}")
                continue

            # ---- Calculs ----
            # 1 Matériel
            cout_materiel += prix_m * longueur

            # 2Travail total (si 1 ouvrier)
            total_hours = duree_h * longueur

            # 3 Durée effective (4 ouvriers en parallèle sur CETTE infra)
            duree_effective = total_hours / WORKERS
            durees_effectives.append(duree_effective)

            # 4 Coût main d'œuvre
            cout_main_oeuvre += total_hours * HOURLY_RATE

            print(f" {infra_type} | Longueur: {longueur} m | "
                  f"Durée effective: {duree_effective:.2f} h | "
                  f"Main d'œuvre: {total_hours * HOURLY_RATE:.2f} €")

        # 5️⃣ Durée totale = le maximum des durées (parallélisme)
        duree_totale = max(durees_effectives) if durees_effectives else 0
        cout_total = cout_materiel + cout_main_oeuvre

        return pd.Series([cout_total, cout_materiel, cout_main_oeuvre, duree_totale])

    except Exception as e:
        print(" Erreur sur :", cluster_infra_str)
        print(e)
        return pd.Series([0, 0, 0, 0])


# --- Application au DataFrame ---
final_df[['cout_total', 'cout_materiel', 'cout_main_oeuvre', 'duree_totale']] = (
    final_df['cluster_infra'].apply(calculer_prix_et_duree)
)

# Vérification du résultat
print(final_df.head())

# Nettoyage
final_df.drop(columns=['state_batiment', 'infra_type'], inplace=True, errors='ignore')

# Sauvegarde
final_df.to_csv("all_for_one_avec_cout.csv", index=False)
print("✅ Fichier sauvegardé avec le parallélisme pris en compte")
