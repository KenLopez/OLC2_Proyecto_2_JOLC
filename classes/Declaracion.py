from classes.ArrayAccess import ArrayAccess
from classes.Value import Value
from classes.Symbol import Symbol
from classes.Tipo import TYPE
class Declaracion:
    def __init__(self, id, val, row, col):
        self.id = id
        self.val = val
        self.row = row
        self.col = col