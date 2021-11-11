from classes.InstruccionC3D import InstruccionC3D
from classes.Tipo import TYPE
from classes.Symbol import Symbol
class Asignacion:
    def __init__(self, id, val, type, typeExp, row, col):
        self.id = id
        self.val = val
        self.type = type
        self.typeExp = typeExp
        self.row = row
        self.col = col
    
    def translate(self, main, ts, scope):
        s = ts.getSymbol(self.id.id, self.typeExp)
        translation = []
        if(s == None):
            s = Symbol(0, None, self.type, None, None, None, None)
        val = self.val.translate(main, ts, scope)
        if(val.type == TYPE.ERROR or (val.type != self.type.val and self.type.val != TYPE.ANY)):
            return translation
        temps = [main.getTemp()]
        translation.append(InstruccionC3D(temps[0], None, 'P', None, s.pos, TYPE.ADDITION))
        translation += val.c3d
        if(val.type != TYPE.BOOL):
            translation.append(InstruccionC3D('stack', temps[0], val.tmp, None, None, TYPE.ASSIGN))
        else:
            ls = main.getLabel()
            for label in val.tmp.lv:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation.append(InstruccionC3D('stack', temps[0], 1, None, None, TYPE.ASSIGN))
            translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.GOTO))
            for label in val.tmp.lf:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation.append(InstruccionC3D('stack', temps[0], 0, None, None, TYPE.ASSIGN))
            translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.LABEL))
        s.type = val.type
        return translation


        