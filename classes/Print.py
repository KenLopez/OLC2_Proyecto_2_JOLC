from classes.Value import Value
from classes.Tipo import TYPE
class Print:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col
        if(val == []):
            self.val.append(Value('', TYPE.TYPESTRING, row, col))
