from classes.Symbol import Symbol
from classes.Tipo import TYPE
from classes.SymbolTable import SymbolTable
from classes.Asignacion import Asignacion
from classes.Value import Value
class Call:
    def __init__(self, id, args, row, col):
        self.id = id
        self.args = args
        self.row = row
        self.col = col