from mesa import Agent

class BiomeCell(Agent):
    def __init__(self, unique_id, model, type="lightgreen"):
        super().__init__(unique_id, model)
        self.type = None
        if type == 'lightgreen':
            self.type = "Upland Pine"
        elif type == 'darkgreen':
            self.type = "Hardwood Bottomland"
        elif type == 'white':
            self.type = 'Pasture'
        elif type == 'blue':
            self.type = "Water"
        elif type == 'brown':
            self.type = "Savannah"