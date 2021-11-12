from classes.Array import Array
from classes.InstruccionC3D import InstruccionC3D
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
class ArrayAccess:
    def __init__(self, id, access, row, col):
        self.id = id
        self.access = access
        self.row = row
        self.col = col
        self.ls = []

    def getRef(self, main, ts, scope):
        translation = ValueC3D(main.getTemp(), TYPE.INT64, [])
        s = self.id.translate(main, ts, scope)
        if(s.type != TYPE.LIST):
            return translation
        translation.c3d += s.c3d
        dim = s.tmp
        tmp = s.tmp.tmp
        ref = 0
        pos = ts.getLength()
        ls = []
        for i in range(0, len(self.access)):
            res = self.access[i].translate(main, ts, scope)
            if(res.type != TYPE.INT64):
                translation = ValueC3D(0, TYPE.INT64, [])
                break
            elif(i != len(self.access)-1 and dim.dim == None):
                translation = ValueC3D(0, TYPE.INT64, [])
                break
            if(main.functions.get('stringLength')==None):
                main.addStringLength()
            translation.c3d += res.c3d
            tmps = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
            labels = [main.getLabel(), main.getLabel(), main.getLabel()]
            ls.append(labels[2])
            translation.c3d += [
                InstruccionC3D(tmps[0], None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D(tmps[1], None, tmps[0], None, 0, TYPE.ADDITION),
                InstruccionC3D('stack', tmps[1], tmp, None, None, TYPE.ASSIGN),
                InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D('stringLength', None, None, None, None, TYPE.CALL),
                InstruccionC3D(tmps[2], None, 'P', None, 1, TYPE.ADDITION),
                InstruccionC3D(tmps[3], None, 'stack', tmps[2], None, TYPE.ASSIGN),
                InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                InstruccionC3D(labels[0], None, res.tmp, None, 1, TYPE.LOWER),
                InstruccionC3D(labels[0], None, res.tmp, None, tmps[3], TYPE.GREATER),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(None, None, 66, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 111, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 117, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 110, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 100, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 115, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 69, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 111, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 10, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(tmps[4], None, tmp, None, res.tmp, TYPE.ADDITION),
                InstruccionC3D(tmps[5], None, tmps[4], None, 1, TYPE.SUBSTRACTION),
                InstruccionC3D(tmps[6], None, 'heap', tmps[5], None, TYPE.ASSIGN)
            ]
            ref = tmps[5]
            tmp = tmps[6]
            dim = dim.dim
            translation.type = dim.type
        translation.c3d.append(InstruccionC3D(translation.tmp, None, ref, None, None, TYPE.ASSIGN))
        self.ls = ls
        return translation

    def translate(self, main, ts, scope):
        translation = ValueC3D(main.getTemp(), TYPE.INT64, [])
        s = self.id.translate(main, ts, scope)
        if(s.type != TYPE.LIST):
            return translation
        translation.c3d += s.c3d
        dim = s.tmp
        tmp = s.tmp.tmp
        pos = ts.getLength()
        ls = []
        for i in range(0, len(self.access)):
            res = self.access[i].translate(main, ts, scope)
            if(res.type != TYPE.INT64):
                translation = ValueC3D(0, TYPE.INT64, [])
                break
            elif(i != len(self.access)-1 and dim.dim == None):
                translation = ValueC3D(0, TYPE.INT64, [])
                break
            if(main.functions.get('stringLength')==None):
                main.addStringLength()
            translation.c3d += res.c3d
            tmps = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
            labels = [main.getLabel(), main.getLabel(), main.getLabel()]
            ls.append(labels[2])
            translation.c3d += [
                InstruccionC3D(tmps[0], None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D(tmps[1], None, tmps[0], None, 0, TYPE.ADDITION),
                InstruccionC3D('stack', tmps[1], tmp, None, None, TYPE.ASSIGN),
                InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D('stringLength', None, None, None, None, TYPE.CALL),
                InstruccionC3D(tmps[2], None, 'P', None, 1, TYPE.ADDITION),
                InstruccionC3D(tmps[3], None, 'stack', tmps[2], None, TYPE.ASSIGN),
                InstruccionC3D('P', None,'P', None, pos, TYPE.SUBSTRACTION),
                InstruccionC3D(labels[0], None, res.tmp, None, 1, TYPE.LOWER),
                InstruccionC3D(labels[0], None, res.tmp, None, tmps[3], TYPE.GREATER),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(None, None, 66, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 111, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 117, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 110, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 100, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 115, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 69, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 111, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(None, None, 10, None, TYPE.CHAR, TYPE.PRINT),
                InstruccionC3D(translation.tmp, None, 0, None, None, TYPE.ASSIGN),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(tmps[4], None, tmp, None, res.tmp, TYPE.ADDITION),
                InstruccionC3D(tmps[5], None, tmps[4], None, 1, TYPE.SUBSTRACTION),
                InstruccionC3D(tmps[6], None, 'heap', tmps[5], None, TYPE.ASSIGN)
            ]
            tmp = tmps[6]
            dim = dim.dim
            translation.type = dim.type
        translation.c3d.append(InstruccionC3D(translation.tmp, None, tmp, None, None, TYPE.ASSIGN))
        for label in ls:
            translation.c3d.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        if(translation.type == TYPE.LIST):
            translation.tmp = Array(translation.tmp, dim.type, dim.dim)
        return translation