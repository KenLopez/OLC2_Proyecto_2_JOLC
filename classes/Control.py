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
        return translation