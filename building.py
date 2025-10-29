class Building:
    
    nb_building = 0
    
    def __init__(self, id_building: str, list_infras: list):
        self.id_building = id_building
        self.list_infras = list_infras
        Building.nb_building += 1
        
    def get_building_difficulty(self):
        return sum(self.list_infras)
    
    def __lt__(self, other_building):
        return self.get_building_difficulty() < other_building.get_building_difficulty()

    def __repr__(self):
        return self.id_building