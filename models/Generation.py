class Generation:
    def __init__(self, id, cromosomas: list, is_min_fn: bool):
        self.id = id
        self.cromosomas = cromosomas
        self.better = None
        self.worst = None
        self.prom = 0
        self.is_min_fn = is_min_fn
        self.define_fitness()
        self.define_prom()
    def define_prom(self):
        result = 0
        for cromosoma in self.cromosomas:
            result += cromosoma.fx
        self.prom = result / len(self.cromosomas)

    def define_fitness(self):
        if self.is_min_fn:
            self.better=self.min_val()
            self.worst=self.max_val()
        else:
            self.better = self.max_val()
            self.worst = self.min_val()

    def min_val(self):
        return min(self.cromosomas, key=lambda chromosoma: chromosoma.fx)

    def max_val(self):
        return max(self.cromosomas, key=lambda chromosoma: chromosoma.fx)
    def __str__(self):
        return f"Generation(id={self.id}, better_fitness={self.better.fx}, worst_fitness={self.worst.fx}, prom={self.prom}, type_resolution={'min' if self.is_min_fn else 'max'})"
