from classes.Tipo import TYPE
from classes.InstruccionC3D import InstruccionC3D
from classes.ValueC3D import ValueC3D

class Value:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col

    def translate(self, main, ts):
        val = ValueC3D(0, self.type, [])
        if(self.type == TYPE.INT64 or self.type == TYPE.FLOAT64):
            val.tmp = self.val
        elif(self.type == TYPE.CHAR):
            val.tmp = ord(self.val)
        elif(self.type == TYPE.BOOL):
            val.tmp = int(self.val)
        elif(self.type == TYPE.STRING):
            val.tmp = main.getTemp()
            val.c3d.append(InstruccionC3D(val.tmp, None, 'H', None, None, TYPE.ASSIGN))
            for char in self.val:
                val.c3d.append(InstruccionC3D('heap', 'H', ord(char), None, None, TYPE.ASSIGN))
                val.c3d.append(InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION))
            val.c3d.append(InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN))
            val.c3d.append(InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION))
        return val



