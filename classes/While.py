from classes.SymbolTable import SymbolTable
from classes.Value import Value
from classes.Tipo import TYPE
class While:
    def __init__(self, condition, instructions, row, col):
        self.condition = condition
        self.instructions = instructions
        self.row = row
        self.col = col