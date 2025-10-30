
import pandas as pd
import ast
from jointure import calculer_prix_et_duree  # on réutilise ta fonction existante

#calculer la difficulte de reparation d'un batiment qui est duree totale * prix total / nombre de maisons 
#puis on compare les batiments entre eux selon cette difficulte pour difinire l'ordre de reparation
#a chaque itiration on repare le batiment le plus facile a reparer (le moins difficile)
#on suprime ce batiment de la liste et on recommence jusqu'a ce que tous les batiments soient reparer
#et on supprime l'infrastructure reparer de la liste des infrastructures a reparer qui se trouve dans le dictionnaire de la colonne culster_infra
#si le dictionnaire est vide on supprime le batiment de la liste des batiments a reparer
#on refait le calcul des couts puis le calcul de la difficulte de reparation pour les batiments restants


# Chargement des données
data = pd.read_csv("all_for_one_avec_cout.csv")

# Convertir le dictionnaire stocké en texte
data["cluster_infra"] = data["cluster_infra"].apply(ast.literal_eval)

# Définir la priorité du type de bâtiment (plus petit = plus prioritaire)
priorite_map = {
    "hôpital": 1,
    "école": 2
}
# Les autres auront priorité 3 par défaut
data["priorite"] = data["type_batiment"].map(priorite_map).fillna(3)

ordre_reparation = []
iteration = 1

while not data.empty:
    # Recalculer coût et durée après suppression d'infras
    data[['cout_total', 'duree_totale']] = data['cluster_infra'].apply(calculer_prix_et_duree)
    data['difficulte'] = data['duree_totale'] * data['cout_total'] / data['nb_maisons']
    
    # Trier d'abord par priorité, puis par difficulté
    data = data.sort_values(by=['priorite', 'difficulte'], ascending=[True, True]).reset_index(drop=True)
    
    # Choisir le bâtiment le plus prioritaire et le moins difficile
    batiment_facile = data.iloc[0]
    id_facile = batiment_facile['id_batiment']
    infra_reparees = list(batiment_facile['cluster_infra'].keys())
    
    # Supprimer ces infrastructures dans tout le dataset
    data['cluster_infra'] = data['cluster_infra'].apply(
        lambda d: {k: v for k, v in d.items() if k not in infra_reparees}
    )
    
    # Identifier tous les bâtiments complètement réparés
    batiments_repares = data.loc[data['cluster_infra'].apply(len) == 0, 'id_batiment'].tolist()
    
    # Ajouter à la liste des réparations
    for bid in batiments_repares:
        ordre_reparation.append((iteration, bid))
    
    # Supprimer les bâtiments réparés
    data = data[data['cluster_infra'].apply(len) > 0]
    
    iteration += 1

# Créer le DataFrame final
ordre_df = pd.DataFrame(ordre_reparation, columns=['ordre', 'id_batiment'])
ordre_df = ordre_df.drop_duplicates(subset='id_batiment', keep='first').reset_index(drop=True)
ordre_df.to_csv("ordre_reparation_priorisee.csv", index=False)

print(f"✅ {len(ordre_df)} bâtiments réparés au total (sur 85 attendus)")
print(ordre_df.head(15))