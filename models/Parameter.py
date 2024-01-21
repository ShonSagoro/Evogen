import math


class Parameter:
    def __init__(self, min_limit, max_limit, pob, pob_max, ind_mut_prob, gen_mut_prob, generations,
                 resolution_ideal, cant_ind_cross, is_min_solution):
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.pob = pob
        self.pob_max = pob_max
        self.indMutProb = ind_mut_prob
        self.genMutProb = gen_mut_prob
        self.range = self.define_range()
        self.generations = generations
        self.resolution_ideal = resolution_ideal
        self.cant_ind_cross = cant_ind_cross
        self.jumps = self.define_jumps()
        self.points = self.define_points()
        self.bits = self.define_bits()
        self.is_min_solution = is_min_solution
        self.better_delta= self.define_difx()

    def define_range(self) -> int:
        return self.max_limit - self.min_limit

    def define_difx(self):
        dfx=float(f"{self.range / (2 ** self.bits - 1):.4f}")
        if dfx>self.resolution_ideal:
            dfx=self.resolution_ideal
        return dfx

    # bits=log base 2 (points)
    def define_bits(self):
        return int(math.log2(self.points)) + 1

    # range / resolution_ideal
    def define_jumps(self):
        return int(self.range / self.resolution_ideal)

    # jumps + 1
    def define_points(self):
        return int(self.jumps + 1)

    def __str__(self):
        return (f"min_limit: {self.min_limit}, max_limit: {self.max_limit}, pob: {self.pob}, "
                f"pob_max: {self.pob_max}, ind_mut_prob: {self.indMutProb}, "
                f"gen_mut_prob: {self.genMutProb}, range: {self.range}"
                f"generations: {self.generations}, resolution_ideal: {self.resolution_ideal}, "
                f"cant_ind_cross: {self.cant_ind_cross}, jumps: {self.jumps}, points: {self.points}, "
                f"bits: {self.bits}")
