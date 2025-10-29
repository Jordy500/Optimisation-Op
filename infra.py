class Infra:
    
    nb_infras = 0

    def __init__(self, infra_id: str, lenght: float, infra_type: str, nb_houses: int, price: float, time: float):
        self.infra_id = infra_id
        self.lenght = lenght
        self.infra_type = infra_type
        self.nb_houses = nb_houses
        self.price = price
        self.time = time
        Infra.nb_infras += 1
        
    def repair_infra(self):
        self.infra_type = "infra_intact"
        
    def get_infra_difficulty(self):
        if self.infra_type == "infra_intact":
            return 0
        else:
            return (self.price * self.time)/ self.nb_houses

    def __radd__(self, other_object):
        return self.get_infra_difficulty() + other_object
    
    
if __name__ == "__main__":
    infra_jordan = 