from classes.Array import Array
from classes.LogicC3D import LogicC3D
from classes.Tipo import TYPE
from classes.InstruccionC3D import InstruccionC3D
from classes.ValueC3D import ValueC3D

class Value:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col

    def translate(self, main, ts, scope):
        val = ValueC3D(0, self.type, [])
        if(self.type == TYPE.INT64 or self.type == TYPE.FLOAT64):
            val.tmp = self.val
        elif(self.type == TYPE.CHAR):
            val.tmp = ord(self.val)
        elif(self.type == TYPE.BOOL):
            lv = main.getLabel()
            lf = main.getLabel()
            val.tmp = LogicC3D([lv], [lf])
            gv = InstruccionC3D(lv, None, None, None, None, TYPE.GOTO)
            gf = InstruccionC3D(lf, None, None, None, None, TYPE.GOTO)
            if(self.val):
                val.c3d += [gv, gf]
            else:
                val.c3d += [gf, gv]
        elif(self.type == TYPE.STRING):
            val.tmp = main.getTemp()
            val.c3d.append(InstruccionC3D(val.tmp, None, 'H', None, None, TYPE.ASSIGN))
            for char in self.val:
                val.c3d.append(InstruccionC3D('heap', 'H', ord(char), None, None, TYPE.ASSIGN))
                val.c3d.append(InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION))
            val.c3d.append(InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN))
            val.c3d.append(InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION))
        elif(self.type == TYPE.RANGE):
            izq = self.val[0].translate(main, ts, scope)
            der = self.val[1].translate(main, ts, scope)
            if(izq.type != TYPE.INT64 or der.type != TYPE.INT64):
                val.tmp = [0, 0]
            else:
                val.tmp = [izq.tmp, der.tmp]
            val.c3d += izq.c3d + der.c3d
        elif(self.type == TYPE.LIST):
            tmps = []
            types = Array(0, TYPE.NOTHING, None)
            for value in self.val:
                res = value.translate(main, ts, scope)
                val.c3d += res.c3d
                tmp = 0
                if(res.type != TYPE.LIST):
                    if(types.type == TYPE.NOTHING):
                        types.type = res.type
                    tmps.append(res.tmp)
                else:
                    if(types.type == TYPE.NOTHING):
                        types.type = res.type
                        types.dim = res.tmp
                    tmps.append(res.tmp.tmp)
            types.tmp = main.getTemp()
            val.c3d.append(InstruccionC3D(types.tmp, None, 'H', None, None, TYPE.ASSIGN))
            for tmp in tmps:
                val.c3d += [
                    InstruccionC3D('heap', 'H', tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
                ]
            val.c3d += [
                    InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN),
                    InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
                ]
            val.tmp = types
        return val



