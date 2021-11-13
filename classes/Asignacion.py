from classes.Array import Array
from classes.ArrayAccess import ArrayAccess
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
    
    def checkListTypes(self, arr1, arr2):
        if(arr1.dim == None and arr2.dim == None):
            return arr1.type == arr2.type
        elif(arr1.type != arr2.type):
            return False
        else:
            return self.checkListTypes(arr1.dim, arr2.dim)
    
    def translate(self, main, ts, scope):
        translation = []
        if(isinstance(self.id, ArrayAccess)):
            s = self.id.getRef(main, ts, scope)
            translation += s.c3d
            val = self.val.translate(main, ts, scope)
            translation += val.c3d
            if(val.type == TYPE.BOOL):
                ls = main.getLabel()
                for label in val.tmp.lv:
                    translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.append(InstruccionC3D('heap', s.tmp, 1, None, None, TYPE.ASSIGN))
                translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.GOTO))
                for label in val.tmp.lf:
                    translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.append(InstruccionC3D('heap', s.tmp, 0, None, None, TYPE.ASSIGN))
                translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.LABEL))
            elif(val.type == TYPE.LIST):
                translation.append(InstruccionC3D('heap', s.tmp, val.tmp.tmp, None, None, TYPE.ASSIGN))
                s.ext = val.tmp.dim
            else:
                translation.append(InstruccionC3D('heap', s.tmp, val.tmp, None, None, TYPE.ASSIGN))
            for label in self.id.ls:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            return translation
        else:
            s = ts.getSymbol(self.id.id, self.typeExp)
            if(s == None):
                s = Symbol(0, None, self.type, None, None, None, None)
            val = self.val.translate(main, ts, scope)
            if(val.type == TYPE.LIST and self.type.val == TYPE.LIST):
                check = self.checkListTypes(val.tmp, self.type.type)
                if(not check):
                    return translation
            else:
                if(self.type.val != TYPE.ANY and val.type != self.type.val):
                    return translation
            temps = [main.getTemp()]
            translation.append(InstruccionC3D(temps[0], None, 'P', None, s.pos, TYPE.ADDITION))
            translation += val.c3d
            if(val.type == TYPE.BOOL):
                ls = main.getLabel()
                for label in val.tmp.lv:
                    translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.append(InstruccionC3D('stack', temps[0], 1, None, None, TYPE.ASSIGN))
                translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.GOTO))
                for label in val.tmp.lf:
                    translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.append(InstruccionC3D('stack', temps[0], 0, None, None, TYPE.ASSIGN))
                translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.LABEL))
            elif(val.type == TYPE.LIST):
                translation.append(InstruccionC3D('stack', temps[0], val.tmp.tmp, None, None, TYPE.ASSIGN))
                s.ext = val.tmp
            else:
                translation.append(InstruccionC3D('stack', temps[0], val.tmp, None, None, TYPE.ASSIGN))
            s.type = val.type
            if(s.type != TYPE.LIST):
                s.ext = None
            return translation


        