from classes.StructAccess import StructAccess
from classes.ArrayAccess import ArrayAccess
from classes.Value import Value
from classes.Symbol import Symbol
from classes.Tipo import TYPE
class Asignacion:
    def __init__(self, id, val, type, typeExp, row, col):
        self.id = id
        self.val = val
        self.type = type
        self.typeExp = typeExp
        self.row = row
        self.col = col