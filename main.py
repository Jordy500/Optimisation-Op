import pandas as pd
import ast
from jointure import calculer_prix_et_duree  # ta fonction existante

# Charger les données
final_df = pd.read_csv("all_for_one_avec_cout.csv")

# Fonction pour calculer la difficulté d'un batiment
def calculer_difficulte(row):
    nb_maisons = row.get('nb_maisons', 1)  # éviter division par 0
    return (row['duree_totale'] * row['cout_total']) / nb_maisons

# Initialisation
batiments_a_reparer = final_df.copy()
batiments_a_reparer['difficulte'] = batiments_a_reparer.apply(calculer_difficulte, axis=1)

ordre_reparation = []

# Itération jusqu'à ce que tous les batiments soient réparés
while not batiments_a_reparer.empty:
    # Prioriser hôpitaux et écoles
    mask_priorite = batiments_a_reparer['type_batiment'].isin(['hôpital', 'école'])
    
    if mask_priorite.any():
        # On prend le moins difficile parmi les priorités
        batiment_courant = batiments_a_reparer[mask_priorite].nsmallest(1, 'difficulte')
    else:
        # Sinon le moins difficile de tous
        batiment_courant = batiments_a_reparer.nsmallest(1, 'difficulte')

    idx = batiment_courant.index[0]
    ordre_reparation.append(idx)  # Ajouter au plan de réparation

    # --- Supprimer l'infrastructure réparée ---
    cluster_infra_str = batiments_a_reparer.at[idx, 'cluster_infra']
    if isinstance(cluster_infra_str, str):
        cluster_dict = ast.literal_eval(cluster_infra_str)
    else:
        cluster_dict = cluster_infra_str

    # Supprimer toutes les infrastructures de ce batiment
    cluster_dict.clear()
    batiments_a_reparer.at[idx, 'cluster_infra'] = cluster_dict

    # --- Recalculer les coûts pour ce batiment ---
    couts = calculer_prix_et_duree(cluster_dict)
    batiments_a_reparer.loc[idx, ['cout_total', 'cout_materiel', 'cout_main_oeuvre', 'duree_totale']] = couts

    # --- Recalculer la difficulté pour les batiments restants ---
    batiments_a_reparer['difficulte'] = batiments_a_reparer.apply(calculer_difficulte, axis=1)

    # --- Supprimer les batiments dont le cluster est vide ---
    batiments_a_reparer = batiments_a_reparer[batiments_a_reparer['cluster_infra'].apply(lambda x: bool(ast.literal_eval(x)) if isinstance(x, str) else bool(x))]

# Résultat final : ordre de réparation
final_order_df = final_df.loc[ordre_reparation].copy()
final_order_df.reset_index(drop=True, inplace=True)

# Sauvegarde
final_order_df.to_csv("ordre_reparation.csv", index=False)
print("✅ Ordre de réparation calculé et sauvegardé")
