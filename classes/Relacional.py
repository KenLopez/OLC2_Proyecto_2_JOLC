from classes.Value import Value
from classes.Tipo import TYPE

class Relacional:
    def __init__(self, expIzq, expDer, type, row, col):
        self.expIzq = expIzq
        self.expDer = expDer
        self.type = type
        self.row = row
        self.col = col