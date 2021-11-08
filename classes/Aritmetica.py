from classes.InstruccionC3D import InstruccionC3D
from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D

class Aritmetica:

    def __init__(self, expIzq, expDer, type, row, col):
        self.expIzq = expIzq
        self.expDer = expDer
        self.type = type
        self.row = row
        self.col = col
    
    def checkTypes(self, izq, der):
        if(
            self.type == TYPE.ADDITION 
            or self.type == TYPE.SUBSTRACTION 
            or self.type == TYPE.MODULUS
        ):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
                elif(der.type == TYPE.INT64):
                    return TYPE.INT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.FLOAT64 or der.type == TYPE.INT64):
                    return TYPE.FLOAT64
        elif(self.type == TYPE.MULTIPLICATION):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.INT64):
                    return TYPE.INT64
                elif(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.FLOAT64 or der.type == TYPE.INT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.STRING and der.type == TYPE.STRING):
                return TYPE.STRING
        elif(self.type == TYPE.DIVISION):
            if(izq.type == TYPE.INT64 or izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.INT64 or der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
        elif(self.type == TYPE.NEGATIVE):
            if(izq.type == TYPE.INT64 or izq.type == TYPE.FLOAT64):
                return izq.type
        elif(self.type == TYPE.POWER):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.INT64):
                    return TYPE.INT64
                elif(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.INT64 or der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.STRING and der.type == TYPE.INT64):
                return TYPE.STRING
        return TYPE.ERROR
    
    def translate(self, main, ts): 
        izq = self.expIzq.translate(main, ts)
        der = ValueC3D(None, TYPE.NOTHING, [])
        if(self.expDer != None):
            der  = self.expDer.translate(main, ts)
        translation = ValueC3D(0, self.checkTypes(izq, der), [])
        if(translation.type == TYPE.ERROR): 
            return translation
        translation.tmp = main.getTemp()
        translation.c3d += izq.c3d
        translation.c3d += der.c3d
        if(translation.type == TYPE.INT64 or translation.type == TYPE.FLOAT64):
            ins = InstruccionC3D(translation.tmp, None, izq.tmp, None, der.tmp, self.type)
            if(self.type == TYPE.MODULUS or self.type == TYPE.DIVISION):
                if(self.type == TYPE.MODULUS):
                    for element in main.imports:
                        if(element == "math"):
                            break
                    else:
                        main.imports.append("math")
                lv = main.getLabel()
                ls = main.getLabel()
                translation.c3d += [
                    InstruccionC3D(lv, None, der.tmp, None, 0, TYPE.DIFFERENT),
                    InstruccionC3D(None, None, 77, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 97, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 116, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 104, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 69, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 111, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 10, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(translation.tmp, None, 0, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                    InstruccionC3D(lv, None, None, None, None, TYPE.LABEL),
                    ins,
                    InstruccionC3D(ls, None, None, None, None, TYPE.LABEL),
                ]
            elif(self.type == TYPE.POWER):
                if(main.functions.get('numberPower')==None):
                    main.addNumberPower()
                tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
                pos = ts.getLength()
                translation.c3d += [
                    InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[1], izq.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D(tmp[2], None, tmp[0], None, 1, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[2], der.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('numberPower', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[3], None, 'P', None, 2, TYPE.ADDITION),
                    InstruccionC3D(tmp[4], None, 'stack', tmp[3], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                ]
                translation.tmp = tmp[4]
            elif(self.type == TYPE.NEGATIVE):
                translation.c3d.append(InstruccionC3D(translation.tmp, None, izq.tmp, None, -1, TYPE.MULTIPLICATION))
            else:
                translation.c3d.append(ins)
        elif(translation.type == TYPE.STRING):
            if(self.type == TYPE.MULTIPLICATION):
                if(main.functions.get('joinStrings')==None):
                    main.addJoinStrings()
                tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
                pos = ts.getLength()
                translation.c3d += [
                    InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[1], izq.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D(tmp[2], None, tmp[0], None, 1, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[2], der.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('joinStrings', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[3], None, 'P', None, 2, TYPE.ADDITION),
                    InstruccionC3D(tmp[4], None, 'stack', tmp[3], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                ]
                translation.tmp = tmp[4]
            elif(self.type == TYPE.POWER):
                if(main.functions.get('repeatStrings')==None):
                    main.addRepeatStrings()
                tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
                pos = ts.getLength()
                translation.c3d += [
                    InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[1], der.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D(tmp[2], None, tmp[0], None, 1, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp[2], izq.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('repeatStrings', None, None, None, None, TYPE.CALL),
                    InstruccionC3D(tmp[3], None, 'P', None, 2, TYPE.ADDITION),
                    InstruccionC3D(tmp[4], None, 'stack', tmp[3], None, TYPE.ASSIGN),
                    InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                ]
                translation.tmp = tmp[4]
        return translation
            
            
        
                    