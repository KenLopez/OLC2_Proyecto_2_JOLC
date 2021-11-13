from classes.Array import Array
from classes.LogicC3D import LogicC3D
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
from classes.InstruccionC3D import InstruccionC3D
class Call:
    def __init__(self, id, args, row, col):
        self.id = id
        self.args = args
        self.row = row
        self.col = col
    
    def translate(self, main, ts, scope):
        translation = ValueC3D(0, TYPE.INT64, [])
        f = main.definitions.get(self.id)
        if(len(self.args) != len(f.params)):
            return translation
        pos = ts.getLength()
        sim = main.getTemp()
        translation.c3d.append(InstruccionC3D(sim, None, 'P', None, pos, TYPE.ADDITION))
        for i in range(len(self.args)):
            res = self.args[i].translate(main, ts, scope)
            if(res.type != f.params[i].type.val):
                return translation
            tmp = main.getTemp()
            translation.c3d.append(InstruccionC3D(tmp, None, sim, None, i, TYPE.ADDITION))
            translation.c3d += res.c3d
            if(res.type == TYPE.BOOL):
                ntmp = main.getTemp()
                ls = main.getLabel()
                translation.c3d += [
                    InstruccionC3D(res.tmp.lv, None, None, None, None, TYPE.LABEL),
                    InstruccionC3D(ntmp, None, 1, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                    InstruccionC3D(res.tmp.lf, None, None, None, None, TYPE.LABEL),
                    InstruccionC3D(ntmp, None, 0, None, None, TYPE.ASSIGN),
                    InstruccionC3D(ls, None, None, None, None, TYPE.LABEL),
                ]
            elif(res.type == TYPE.LIST):
                ntmp = res.tmp.tmp
            else:
                ntmp = res.tmp
            translation.c3d.append(InstruccionC3D('stack', tmp, ntmp, None, None, TYPE.ASSIGN))
        r = f.ts.getSymbol('#', TYPE.NOTHING)
        tmps = [main.getTemp(), main.getTemp()]
        translation.c3d += [
            InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
            InstruccionC3D(f'{self.id}_', None, None, None, None, TYPE.CALL),
            InstruccionC3D(tmps[0], None, 'P', None, r.pos, TYPE.ADDITION),
            InstruccionC3D(tmps[1], None, 'stack', tmps[0], None, TYPE.ASSIGN),
            InstruccionC3D(tmps[0], None, 'P', None, pos, TYPE.SUBSTRACTION),
        ]
        translation.type = r.type
        translation.tmp = tmps[1]
        if(translation.type == TYPE.BOOL):
            lv = main.getLabel()
            lf = main.getLabel()
            translation.tmp = LogicC3D([lv], [lf])
            translation.c3d += [
                InstruccionC3D(lv, None, tmps[1], None, 1, TYPE.EQUAL),
                InstruccionC3D(lf, None, None, None, None, TYPE.GOTO),
            ]
        elif(translation.type == TYPE.LIST):
            translation.tmp = Array(tmps[1], r.ext.type, r.ext.dim)
        return translation
        
