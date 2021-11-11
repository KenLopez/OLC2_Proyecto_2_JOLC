from classes.Value import Value
from classes.Tipo import TYPE
class StructAccess:
    def __init__(self, id, access, row, col):
        self.val = id
        self.access = access
        self.row = row
        self.col = col