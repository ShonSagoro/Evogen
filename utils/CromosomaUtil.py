from models.Generation import Generation
from models.Parameter import Parameter
import random

cromosomas = []
generation = []
function=

def model(x):
    return x**2 -5*x + 6

parameter = Parameter(1, 7, 4, 8, 0.90, 0.30, 0.40)


def make_pob_init():
    for i in range(0, parameter.pob):
        pob = random.randint(1, 31)
        cromosomas.append(pob)

def get_x()

def init(iter):
    make_pob_init()
    for i in range(0, iter):
        generation = Generation(i, cromosomas)
