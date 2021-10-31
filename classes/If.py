from classes.SymbolTable import SymbolTable
from classes.Value import Value
from classes.Tipo import TYPE
class If:
    def __init__(self, conditions, instructions, elseinstructions, row, col):
        self.conditions = conditions
        self.instructions = instructions
        self.elseinstructions = elseinstructions
        self.row = row
        self.col = col