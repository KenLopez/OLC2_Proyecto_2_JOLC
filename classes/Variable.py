from classes.Array import Array
from classes.InstruccionC3D import InstruccionC3D
from classes.LogicC3D import LogicC3D
from classes.Tipo import TYPE
from classes.Value import Value
from classes.ValueC3D import ValueC3D


class Variable:
    def __init__(self, id, row, col):
        self.id = id
        self.row = row
        self.col = col
    
    def translate(self, main, ts, scope):
        s = ts.getSymbol(self.id, TYPE.ANY)
        translation = ValueC3D(0, TYPE.INT64, [])
        if(s == None or s.type == TYPE.NOTHING):
            return translation
        translation.type = s.type
        temps = [main.getTemp(), main.getTemp()]
        translation.c3d += [
                InstruccionC3D(temps[0], None, 'P', None, s.pos, TYPE.ADDITION),
                InstruccionC3D(temps[1], None, 'stack', temps[0], None, TYPE.ASSIGN),
            ]
        if(translation.type == TYPE.BOOL):
            lv = main.getLabel()
            lf = main.getLabel()
            translation.c3d += [
                InstruccionC3D(lv, None, temps[1], None, 1, TYPE.EQUAL),
                InstruccionC3D(lf, None, None, None, None, TYPE.GOTO),
            ]
            translation.tmp = LogicC3D([lv], [lf])
        elif(translation.type == TYPE.LIST):
            translation.tmp = Array(temps[1], s.type, s.ext)
        else:
            translation.tmp = temps[1]
        return translation
            
            
        
