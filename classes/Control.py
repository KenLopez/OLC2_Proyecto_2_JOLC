from classes.ControlC3D import ControlC3D
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
from classes.InstruccionC3D import InstruccionC3D
class Control:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col

    def translate(self, main, ts, scope):
        translation = []
        if(self.type == TYPE.BREAK or self.type == TYPE.CONTINUE):
            if(str(scope).__contains__('FOR') or str(scope).__contains__('WHILE')):
                control = ControlC3D(main.getLabel(), self.type)
                translation = ValueC3D([control], TYPE.CONTROL, [])
                translation.c3d.append(InstruccionC3D(control.label, None, None, None, None, TYPE.GOTO))
        elif(self.type == TYPE.RETURN):
            if(str(scope).__contains__('FUNCTION')):
                control = ControlC3D(main.getLabel(), self.type)
                translation = ValueC3D([control], TYPE.CONTROL, [])
                if(self.val != None):
                    s = ts.getSymbol('#', TYPE.NOTHING)
                    tmp = main.getTemp()
                    translation.c3d.append(InstruccionC3D(tmp, None, 'P', None, s.pos, TYPE.ADDITION))
                    res = self.val.translate(main, ts, scope)
                    translation.c3d += res.c3d
                    if(res.type == TYPE.BOOL):
                        ls = main.getLabel()
                        translation.c3d += [
                            InstruccionC3D(res.tmp.lv, None, None, None, None, TYPE.LABEL),
                            InstruccionC3D('stack', tmp, 1, None, None, TYPE.ASSIGN),
                            InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                            InstruccionC3D(res.tmp.lf, None, None, None, None, TYPE.LABEL),
                            InstruccionC3D('stack', tmp, 0, None, None, TYPE.ASSIGN),
                            InstruccionC3D(res.tmp.lf, None, None, None, None, TYPE.LABEL),
                        ]
                    elif(res.type == TYPE.LIST):
                        translation.c3d.append(InstruccionC3D('stack', tmp, res.tmp.tmp, None, None, TYPE.ASSIGN))
                    else:
                        translation.c3d.append(InstruccionC3D('stack', tmp, res.tmp, None, None, TYPE.ASSIGN))
                translation.c3d.append(InstruccionC3D(control.label, None, None, None, None, TYPE.GOTO))
        return translation