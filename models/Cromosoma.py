class Cromosoma:
    def __init__(self, i):
        self.i = i
        self.x = 0
        self.fx = 0
        self.bin = ""
        self.GetBin()

    def GetBin(self):
        binario_str = bin(self.i)[2:]
        self.bin = binario_str

    def SetX(self, x):
        self.x = x

    def SetFx(self, fx):
        self.fx = fx
