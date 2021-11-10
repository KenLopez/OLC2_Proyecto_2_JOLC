from classes.InstruccionC3D import InstruccionC3D
from classes.LogicC3D import LogicC3D
from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D

class Logica:
    def __init__(self, expIzq, expDer, type, row, col):
        self.expIzq = expIzq
        self.expDer = expDer
        self.type = type
        self.row = row
        self.col = col

    def checkTypes(self, izq, der):
        if(izq.type == TYPE.BOOL):
            if(self.type == TYPE.NOT):
                return TYPE.BOOL
            else:
                if(der.type == TYPE.BOOL):
                    return TYPE.BOOL
        return TYPE.ERROR
    
    def translate(self, main, ts):
        izq = self.expIzq.translate(main, ts)
        der = ValueC3D(None, TYPE.NOTHING, [])
        if(self.expDer != None):
            der  = self.expDer.translate(main, ts)
        translation = ValueC3D(LogicC3D([], [], []), self.checkTypes(izq, der), [])
        if(translation.type == TYPE.ERROR): 
            return translation
        if(self.type == TYPE.AND):
            translation.tmp.lv += der.tmp.lv
            translation.tmp.lf += izq.tmp.lf + der.tmp.lf
            translation.c3d += izq.c3d
            for label in izq.tmp.lv:
                translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation.c3d += der.c3d
        if(self.type == TYPE.OR):
            translation.tmp.lv += izq.tmp.lv + der.tmp.lv
            translation.tmp.lf += der.tmp.lf
            translation.c3d += izq.c3d
            for label in izq.tmp.lf:
                translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation.c3d += der.c3d
        if(self.type == TYPE.NOT):
            translation.tmp.lv = izq.tmp.lf
            translation.tmp.lf = izq.tmp.lv
            translation.c3d = izq.c3d
        return translation
