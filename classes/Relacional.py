from classes.InstruccionC3D import InstruccionC3D
from classes.Value import Value
from classes.ValueC3D import ValueC3D
from classes.LogicC3D import LogicC3D
from classes.Tipo import TYPE

class Relacional:
    def __init__(self, expIzq, expDer, type, row, col):
        self.expIzq = expIzq
        self.expDer = expDer
        self.type = type
        self.row = row
        self.col = col
    
    def checkTypes(self, izq, der):
        if(izq.type == TYPE.FLOAT64 or izq.type == TYPE.INT64 or izq.type == TYPE.CHAR or izq.type == TYPE.BOOL):
            if(der.type == TYPE.FLOAT64 or der.type == TYPE.INT64 or der.type == TYPE.CHAR or der.type == TYPE.BOOL):
                return TYPE.FLOAT64
        if(izq.type == TYPE.STRING and der.type == TYPE.STRING):
            return TYPE.STRING
        return TYPE.ERROR
    
    def translate(self, main, ts, scope):
        izq = self.expIzq.translate(main, ts, scope)
        der = self.expDer.translate(main, ts, scope)
        translation = ValueC3D(0, self.checkTypes(izq, der), [])
        if(translation.type == TYPE.ERROR): 
            translation.type == TYPE.INT64
            return translation
        if(translation.type == TYPE.FLOAT64):
            translation.c3d += izq.c3d
            if(izq.type == TYPE.BOOL):
                tmp = main.getTemp()
                ls = main.getLabel()
                for label in izq.tmp.lv:
                    translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))      
                translation.c3d += [
                    InstruccionC3D(tmp, None, 1, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                ]
                for label in izq.tmp.lf:
                    translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.c3d += [
                    InstruccionC3D(tmp, None, 0, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.LABEL),
                ]  
                izq.tmp = tmp
            translation.c3d += der.c3d
            if(der.type == TYPE.BOOL):
                tmp = main.getTemp()
                ls = main.getLabel()
                for label in der.tmp.lv:
                    translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))      
                translation.c3d += [
                    InstruccionC3D(tmp, None, 1, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                ]
                for label in der.tmp.lf:
                    translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
                translation.c3d += [
                    InstruccionC3D(tmp, None, 0, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.LABEL),
                ]  
                der.tmp = tmp
            lv = main.getLabel()
            lf = main.getLabel()
            translation.tmp = LogicC3D([lv], [lf])
            translation.c3d += [
                InstruccionC3D(lv, None, izq.tmp, None, der.tmp, self.type),
                InstruccionC3D(lf, None, None, None, None, TYPE.GOTO)
            ]
        elif(translation.type == TYPE.STRING):
            if(self.type == TYPE.EQUAL or self.type == TYPE.DIFFERENT):
                if(main.functions.get('compareStrings')==None):
                    main.addCompareStrings()
                tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
                lv = main.getLabel()
                lf = main.getLabel()
                translation.tmp = LogicC3D([lv], [lf])
                translation.c3d += izq.c3d
                translation.c3d += der.c3d
                pos = ts.getLength()
                translation.c3d += [
                    InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[1], izq.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D(tmp[2], None, tmp[0], None, 1, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[2], der.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('compareStrings', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[3], None, 'P', None, 2, TYPE.ADDITION),
                    InstruccionC3D(tmp[4], None, 'stack', tmp[3], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                ]
                if(self.type == TYPE.EQUAL):
                    translation.c3d.append(InstruccionC3D(lv, None, tmp[4], None, 1, TYPE.EQUAL))
                if(self.type == TYPE.DIFFERENT):
                    translation.c3d.append(InstruccionC3D(lv, None, tmp[4], None, 0, TYPE.EQUAL))
                translation.c3d.append(InstruccionC3D(lf, None, None, None, None, TYPE.GOTO))
            else:
                if(main.functions.get('stringLength')==None):
                    main.addStringLength()
                tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
                lv = main.getLabel()
                lf = main.getLabel()
                translation.tmp = LogicC3D([lv], [lf])
                translation.c3d += izq.c3d
                translation.c3d += der.c3d
                pos = ts.getLength()
                translation.c3d += [
                    InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[1], izq.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('stringLength', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[2], None, 'P', None, 1, TYPE.ADDITION),
                    InstruccionC3D(tmp[3], None, 'stack', tmp[2], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                    InstruccionC3D(tmp[4], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[5], None, tmp[4], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[5], der.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('stringLength', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[6], None, 'P', None, 1, TYPE.ADDITION),
                    InstruccionC3D(tmp[7], None, 'stack', tmp[6], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                    InstruccionC3D(lv, None, tmp[3], None, tmp[7], self.type),
                    InstruccionC3D(lf, None, None, None, None, TYPE.GOTO),
                ]
        translation.type = TYPE.BOOL
        return translation
