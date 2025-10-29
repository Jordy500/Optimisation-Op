import pandas as pd

# Lire le fichier
df = pd.read_excel("reseau_en_arbre.xlsx")

# Regrouper par infra_id pour créer les "clusters"
grp = df.groupby("infra_id").agg(
    nb_batiments=("id_batiment", lambda x: x.nunique()),
    total_longueur=("longueur", "sum"),
    infra_type=("infra_type", "first"),
    batiments=("id_batiment", lambda x: ",".join(sorted(x.unique()))),
).reset_index()

# Calcul d'une métrique proxy : longueur moyenne par bâtiment
grp["long_per_bat"] = grp["total_longueur"] / grp["nb_batiments"]

# Trier par nb_batiments (desc) puis efficacite (asc)
grp = grp.sort_values(["nb_batiments", "long_per_bat"], ascending=[False, True])

# Sauvegarder le résultat
grp.to_excel("clusters_infra.xlsx", index=False)