class Parameter:
    def __init__(self, min_limit, max_limit, pob, pob_max, cross_prob, ind_mut_prob, gen_mut_prob, bits=5):
        self.min_limit = min_limit
        self.max_limit = max_limit
        self.pob=pob
        self.pob_max=pob_max
        self.bits = bits
        self.crossProb = cross_prob
        self.indMutProb = ind_mut_prob
        self.genMutProb = gen_mut_prob
        self.range = self.get_range()
        self.difX= self.get_difx()

    def get_range(self) -> int:
        return self.max_limit - self.min_limit

    def get_difx(self):
        return self.range/(2**self.bits - 1)
