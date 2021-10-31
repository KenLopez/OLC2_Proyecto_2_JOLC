from classes.Value import Value
from classes.Symbol import Symbol
from classes.Variable import Variable
from classes.Asignacion import Asignacion
from classes.Tipo import TYPE
from classes.SymbolTable import SymbolTable
class For:
    def __init__(self, variable, range, instrucciones, row, col):
        self.variable = variable
        self.range = range
        self.instrucciones = instrucciones
        self.row = row
        self.col = col