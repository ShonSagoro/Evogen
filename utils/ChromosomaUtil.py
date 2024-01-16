import numpy as np
import math
import random

import matplotlib.pyplot as plt

from models.Chromosoma import Chromosoma
from models.Generation import Generation
from models.Parameter import Parameter


class ChromosomaUtil:
    math_function = {
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'pi': np.pi,
        'log': np.log,
        'e': np.e,
        'x': None
    }

    def __init__(self, parameter: Parameter, expression):
        self.parameter = parameter
        self.expression = expression
        self.populations = []
        self.generations = []
        self.generated_figures = []

    def init(self):
        self.populations = []
        self.generations = []
        self.generated_figures = []
        self.make_pob_init()
        self.generations.append(Generation(0, self.populations, self.parameter.is_min_solution))

        for i in range(0, (self.parameter.generations - 2)):
            print(f"generacion: {i}")
            peers = self.define_peers()
            cross_peers = self.cross_peers(peers)
            mutated_peers = self.mutation(cross_peers)
            self.add_mutated_population(mutated_peers)

            self.populations = self.unique_chromosomas()
            purge = self.poda_gen()
            self.populations = purge

            self.generations.append(Generation((i + 1), self.populations, self.parameter.is_min_solution))

        self.chars_report_general()
        self.chars_populations()

    def add_mutated_population(self, mutated_peers):
        new_id = self.populations[-1].id + 1
        mutated_peers = [mutated_peer.set_id_mutate(new_id + i) for i, mutated_peer in enumerate(mutated_peers)]
        self.populations.extend(mutated_peers)

    def get_fx(self, population):
        self.math_function['x'] = population.x
        try:
            result = float(f"{eval(self.expression, self.math_function):.4f}")
            return result
        except Exception as e:
            print(f"Error:{e}")

    def make_pob_init(self):
        self.populations = [
            Chromosoma((i + 1), bin(int(random.uniform(0, self.parameter.points)))[2:].zfill(self.parameter.bits)) for i
            in
            range(self.parameter.pob)]
        self.evaluation_x(self.populations)
        self.evaluation_fx(self.populations)

    def evaluation_x(self, populations):
        for population in populations:
            if population.x is None:
                x = self.get_x(population)
                population.set_x(x)

    def get_x(self, population):
        return float(f"{self.parameter.min_limit + population.i * self.parameter.resolution_ideal:.4f}")

    def evaluation_fx(self, populations):
        for population in populations:
            if population.fx is None:
                result = self.get_fx(population)
                population.set_fx(result)

    def define_peers(self):
        peers = []
        for father1 in self.populations:
            cant_ind = random.uniform(0, self.parameter.cant_ind_cross)
            for _ in range(0, int(cant_ind)):
                father2 = random.choice(self.populations)
                peers.append((father1, father2))
        return peers

    def cross_peers(self, peers):
        descendants = []
        print(f"Cross")
        for peer in peers:
            cross_point = random.randint(1, len(peer[0].bits) - 1)
            chromosoma_1_child_bits = peer[0].bits[:cross_point] + peer[1].bits[cross_point:]
            chromosoma_2_child_bits = peer[1].bits[:cross_point] + peer[0].bits[cross_point:]
            descendants.append((Chromosoma(0, chromosoma_1_child_bits), Chromosoma(0, chromosoma_2_child_bits)))
        print(f"Cross final")
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
        self.evaluation_x(mutated_chromosomes)
        self.evaluation_fx(mutated_chromosomes)
        print(f"Mutation final")
        return mutated_chromosomes

    def gen_mutation(self, child: Chromosoma):
        gens = list(child.bits)
        for i in range(len(gens)):
            if random.uniform(0, 1) < self.parameter.genMutProb:
                j = random.randint(0, len(gens) - 1)
                while j == i:
                    j = random.randint(0, len(gens) - 1)
                gens[i], gens[j] = gens[j], gens[i]
        child.bits = ''.join(gens)
        return Chromosoma(0, child.bits)

    def poda_gen(self):
        print("Podar")
        chromosoma_final = []
        chromosoma_classes = self.define_classes()

        print(list(chromosoma_classes.keys()))

        while len(chromosoma_final) < self.parameter.pob_max and chromosoma_classes:
            random_class = random.choice(list(chromosoma_classes.keys()))
            chromosoma_select = np.random.choice(chromosoma_classes[random_class])
            chromosoma_final.append(chromosoma_select)
            chromosoma_classes[random_class].remove(chromosoma_select)
            if not chromosoma_classes[random_class]:
                del chromosoma_classes[random_class]

        print(len(chromosoma_final))
        return chromosoma_final

    def unique_chromosomas(self):
        return list(set(self.populations))

    def define_classes(self):
        chromosoma_classes = {}
        chromosoma_sorted_fitness = sorted(self.populations, key=lambda chromosoma: chromosoma.fx)
        for chromosoma in chromosoma_sorted_fitness:
            if chromosoma.fx not in chromosoma_classes:
                chromosoma_classes[chromosoma.fx] = []
            chromosoma_classes[chromosoma.fx].append(chromosoma)
        return chromosoma_classes

    def chars_report_general(self):
        plt.style.use('dark_background')

        generation_ids = [(gen.id + 1) for gen in self.generations]
        best_fitness = [gen.better.fx for gen in self.generations]
        worst_fitness = [gen.worst.fx for gen in self.generations]
        average_fitness = [gen.prom for gen in self.generations]

        fig, ax = plt.subplots()

        ax.plot(generation_ids, best_fitness, label='Mejor', marker='o')
        ax.plot(generation_ids, worst_fitness, label='Peor', marker='v')
        ax.plot(generation_ids, average_fitness, label='Promedio', marker='s')

        ax.legend()
        ax.set_xlabel('Generación')
        ax.set_ylabel('Fitness')
        ax.set_title('Resultados por generación')

        self.generated_figures.append(fig)

    def chars_populations(self):
        self.char(self.generations[-1])
        self.char(self.generations[0])

    def char(self, gen):
        plt.style.use('dark_background')
        generation_id = gen.id
        x_values = np.array([chromosome.x for chromosome in gen.chromosomas])
        fx_values = np.array([chromosome.fx for chromosome in gen.chromosomas])

        fig, ax = plt.subplots()

        ax.scatter(x_values, fx_values, s=200, alpha=0.5)

        if gen.better:
            ax.scatter(gen.better.x, gen.better.fx, color='red', s=200, label='Mejor Cromosoma')

        ax.set_xlabel('x')
        ax.set_ylabel('fx')
        ax.set_title(f'Dispersión de fx - Generación {(generation_id + 1)}')

        self.generated_figures.append(fig)
