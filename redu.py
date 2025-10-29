from typing import List

class Infra:
    def __init__(self, infra_id: str, length: float, infra_type: str, nb_houses: int):
        self.infra_id = infra_id
        self.length = length
        self.infra_type = infra_type  # ex : "infra_intacte" ou "a_remplacer"
        self.nb_houses = nb_houses

    # Méthode pour réparer l'infrastructure
    def repair_infra(self):
        self.infra_type = "infra_intacte"

    # Méthode pour obtenir la difficulté d'une réparation ==================================================================================================
    
    
    
    def get_infra_difficulty(self) -> float:
        # Exemple simple : plus c’est long, plus c’est difficile
        base_difficulty = 





    # Permet d'utiliser l’opérateur + entre deux infrastructures (pour additionner les difficultés)
    def __radd__(self, other):
        return other + self.get_infra_difficulty() if isinstance(other, (int, float)) else NotImplemented


class Batiment:
    def __init__(self, id_building: str, list_infras: List[Infra]):
        self.id_building = id_building
        self.list_infras = list_infras  # Liste d’objets Infra

    # Retourne la difficulté totale d’un bâtiment (somme des difficultés de ses infras)
    def get_building_difficulty(self) -> float:
        return sum(self.list_infras)

    # Compare deux bâtiments selon leur difficulté
    def __lt__(self, other) -> bool:
        return self.get_building_difficulty() < other.get_building_difficulty()

    # Vérifie si le bâtiment a de l'électricité
    def has_electricity(self) -> bool:
        return all(infra.infra_type == "infra_intacte" for infra in self.list_infras)

    # Donne un résumé de l'état du bâtiment
    def __repr__(self):
        etat = "⚡ Électrifié" if self.has_electricity() else "À réparer"
        return f"Batiment(id={self.id_building}, état={etat}, difficulté={self.get_building_difficulty():.2f})"
