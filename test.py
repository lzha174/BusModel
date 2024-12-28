import simpy
from typing import Generator, Any
env  = simpy.Environment()

def t1():
    yield env.timeout(5)
    a = 5

def t2():
    yield env.timeout(10)
    b =10

env.process(t1())
env.process(t2())
env.run()

class gWrapper():
    def __init__(self, generator: Generator[int, Any, Any]):
