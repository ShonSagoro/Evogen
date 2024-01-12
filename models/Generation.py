class Generation:
    def __init__(self, id, cromosomas: list):
        self.id=id
        self.cromosomas = cromosomas
        self.better = 0
        self.worst = 0
        self.prom = 0

    def define_prom(self):
        sum = 0
        for cromosoma in self.cromosomas:
            sum += cromosoma.fx
        self.prom = sum / len(self.cromosomas)
