class Chromosoma:
    def __init__(self, id, bits):
        self.id = id
        self.bits = bits
        self.i = self.define_i()
        self.x = None
        self.fx = None

    def __str__(self):
        return f"Cromosoma(id={self.id}, i={self.i}, x={self.x}, fx={self.fx}, bin={self.bits})"

    def define_i(self):
        return int(self.bits, 2)

    def set_x(self, x):
        self.x = x

    def set_fx(self, fx):
        self.fx = fx

    def set_id(self, id):
        self.id=id
