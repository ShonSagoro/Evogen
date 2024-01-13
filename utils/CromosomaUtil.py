import random

from models.Chromosoma import Chromosoma
from models.Generation import Generation
from models.Parameter import Parameter

expression = "x**2 - 5*x + 6"
population_size = 4
population_size_max = 8
cross_prob = 0.90
ind_mut_prob = 0.90
gen_mut_prob = 0.90
generations = 4
min_limit_x = 3
max_limit_x = 7
resolution_ideal = 0.05
points = 31
cant_ind_cross = 2
is_min_solution = False

parameter = Parameter(min_limit_x, max_limit_x, population_size, population_size_max, cross_prob, ind_mut_prob,
                      gen_mut_prob, generations, resolution_ideal, cant_ind_cross)

print(parameter)


class ChromosomaUtil:
    def __init__(self, parameter: Parameter, expression):
        self.parameter = parameter
        self.expression = expression
        self.populations: list[Chromosoma] = []
        self.generations: list[Generation] = []

    def init(self):
        self.make_pob_init()
        self.define_x(self.populations)
        self.define_fx(self.populations)
        self.generations.append(Generation(0, self.populations, is_min_solution))
        for i in range(0, self.parameter.generations):

            peers = self.define_peers()
            cross_peers = self.cross_peers(peers)
            mutated_peers = self.mutation(cross_peers)
            self.define_x(mutated_peers)
            self.define_fx(mutated_peers)

            for mutated_peer in mutated_peers:
                mutated_peer.set_id(self.populations[-1].id + 1)
                self.populations.append(mutated_peer)

            for population in self.populations:
                print(population)

            self.generations.append(Generation((i + 1), self.populations, is_min_solution))

            for generation in self.generations:
                print(generation)

            self.populations = self.unique_chromosomas()
            poda_population=self.poda_gen()
            self.populations=poda_population

            self.populations = sorted(self.populations, key=lambda chromosoma: chromosoma.id)

            print("TODO PODADO")
            for population in self.populations:
                print(population)

        self.generations.append(Generation((parameter.generations+1), self.populations, is_min_solution))
        for generation in self.generations:
            print(generation)
        for population in self.populations:
            print(population)

    def get_fx(self, population):
        try:
            result = eval(self.expression, {'x': population.x})
            return result
        except Exception as e:
            print(f"Error:{e}")

    def make_pob_init(self):
        self.populations = [
            Chromosoma((i + 1), bin(int(random.uniform(0, self.parameter.points)))[2:].zfill(self.parameter.bits)) for i
            in
            range(
                self.parameter.pob)]

    def define_x(self, populations):
        for population in populations:
            if population.x is None:
                x = self.get_x(population)
                population.set_x(x)

    def get_x(self, population):
        return self.parameter.min_limit + population.i * parameter.resolution_ideal

    def define_fx(self, populations):
        for population in populations:
            if population.fx is None:
                result = self.get_fx(population)
                population.set_fx(result)

    def define_peers(self):
        peers = []
        for padre1 in self.populations:
            cant_ind = random.uniform(0, self.parameter.cant_ind_cross)
            for _ in range(0, int(cant_ind)):
                padre2 = random.choice(self.populations)
                peers.append((padre1, padre2))
        for peer in peers:
            print(f"peers: {peer[0]}, {peer[1]}")
        return peers

    def cross_peers(self, peers):
        descendants = []
        for peer in peers:
            chromosoma_1 = peer[0]
            chromosoma_2 = peer[1]
            cross_point = random.randint(1, len(chromosoma_1.bits) - 1)
            chromosoma_1_child_bits = chromosoma_1.bits[:cross_point] + chromosoma_2.bits[cross_point:]
            chromosoma_2_child_bits = chromosoma_2.bits[:cross_point] + chromosoma_1.bits[cross_point:]
            descendants.append((Chromosoma(0, chromosoma_1_child_bits), Chromosoma(0, chromosoma_2_child_bits)))

        for descendant in descendants:
            print(f'croosover: {descendant[0]}, {descendant[1]}')
        return descendants

    def mutation(self, descendants):
        mutated_chromosomes = []
        for descendant in descendants:
            for gen in descendant:
                if random.uniform(0, 1) < self.parameter.indMutProb:
                    mut_gen = self.gen_mutation(gen)
                    mutated_chromosomes.append(mut_gen)
                else:
                    mutated_chromosomes.append(gen)

        return mutated_chromosomes

    def gen_mutation(self, child: Chromosoma):
        print(f"child before mutated: {child}")
        gens = list(child.bits)
        for i in range(len(gens)):
            if random.uniform(0, 1) < self.parameter.genMutProb:
                j = random.randint(0, len(gens) - 1)
                while j == i:
                    j = random.randint(0, len(gens) - 1)
                gens[i], gens[j] = gens[j], gens[i]
        child.bits = ''.join(gens)
        child_mutated = Chromosoma(0, child.bits)
        print(f"child mutated: {child_mutated}")
        return child_mutated

    def poda_gen(self):
        chromosoma_final = []
        chromosoma_classes=self.define_classes()

        while len(chromosoma_final) <= parameter.pob_max and len(chromosoma_classes.keys())>0:
            random_class=random.choice(list(chromosoma_classes.keys()))
            chromosoma_select= chromosoma_classes[random_class]
            chromosoma_final.extend(chromosoma_select)
            del chromosoma_classes[random_class]

        return chromosoma_final
    def unique_chromosomas(self):
        unique_population_set = set()
        unique_population = []
        for chromosoma in self.populations:
            if chromosoma.i not in unique_population:
                unique_population_set.add(chromosoma)
                unique_population.append(chromosoma)
        return unique_population

    def define_classes(self):
        chromosoma_classes = {}
        chromosoma_sorted_fitness = sorted(self.populations, key=lambda chromosoma: chromosoma.fx)

        for chromosoma in chromosoma_sorted_fitness:
            if chromosoma.fx not in chromosoma_classes:
                chromosoma_classes[chromosoma.fx] = []
            chromosoma_classes[chromosoma.fx].append(chromosoma)
        return chromosoma_classes

chromosomaUtil = ChromosomaUtil(parameter, expression)
chromosomaUtil.init()
