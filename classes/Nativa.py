from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
from classes.InstruccionC3D import InstruccionC3D


class Nativa:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col 
    
    def translate(self, main, ts, scope):
        translation = ValueC3D(0, TYPE.INT64, [])
        if(self.type == TYPE.TRUNCATE):
            if(len(self.val)!=1):
                return translation
            val = self.val[0].translate(main, ts, scope)
            if(val.type != TYPE.FLOAT64):
                return translation
            translation.type = TYPE.INT64
            translation.c3d += val.c3d
            for element in main.imports:
                if(element == "math"):
                    break
            else:
                main.imports.append("math")
            tmps = [main.getTemp(), main.getTemp()]
            translation.c3d += [
                InstruccionC3D(tmps[0], None, val.tmp, None, 1, TYPE.MODULUS),
                InstruccionC3D(tmps[1], None, val.tmp, None, tmps[0], TYPE.SUBSTRACTION),
            ]
            translation.tmp = tmps[1]
            return translation
        func = ''
        var = None
        if(self.type == TYPE.LOWERCASE):
            if(len(self.val)!=1):
                return translation
            val = self.val[0].translate(main, ts, scope)
            if(val.type != TYPE.STRING):
                return translation
            translation.type = TYPE.STRING
            func = 'lowercase'
            var = val.tmp
            if(main.functions.get(func)==None):
                main.addToLower()
        elif(self.type == TYPE.UPPERCASE):
            if(len(self.val)!=1):
                return translation
            val = self.val[0].translate(main, ts, scope)
            if(val.type != TYPE.STRING):
                return translation
            translation.type = TYPE.STRING
            func = 'uppercase'
            var = val.tmp
            if(main.functions.get(func)==None):
                main.addToUpper()
        elif(self.type == TYPE.LENGTH):
            if(len(self.val)!=1):
                return translation
            val = self.val[0].translate(main, ts, scope)
            if(val.type == TYPE.STRING or val.type == TYPE.LIST):
                func = 'stringLength'
                if(val.type == TYPE.STRING):
                    var = val.tmp
                else:
                    var = val.tmp.tmp
            else:
                return translation
            translation.type = TYPE.INT64
            if(main.functions.get(func)==None):
                main.addStringLength()
        tmp = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
        translation.c3d += val.c3d
        pos = ts.getLength()
        translation.c3d += [
            InstruccionC3D(tmp[0], None, 'P', None, pos, TYPE.ADDITION),
            InstruccionC3D(tmp[1], None, tmp[0], None, 0, TYPE.ADDITION),
            InstruccionC3D('stack', tmp[1], var, None, None, TYPE.ASSIGN),
            InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
            InstruccionC3D(func, None, None, None, None, TYPE.CALL),
            InstruccionC3D(tmp[2], None, 'P', None, 1, TYPE.ADDITION),
            InstruccionC3D(tmp[3], None, 'stack', tmp[2], None, TYPE.ASSIGN),
            InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
        ]
        translation.tmp = tmp[3]
        return translation
            
