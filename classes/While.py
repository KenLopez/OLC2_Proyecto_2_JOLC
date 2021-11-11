from classes.Asignacion import Asignacion
from classes.InstruccionC3D import InstruccionC3D
from classes.LogicC3D import LogicC3D
from classes.Symbol import Symbol
from classes.SymbolTable import SymbolTable
from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
class While:
    def __init__(self, condition, instructions, row, col):
        self.condition = condition
        self.instructions = instructions
        self.row = row
        self.col = col
        self.ts = None

    def getSymbols(self, scope):
        pos = self.ts.getLength()
        for instruccion in self.instructions:
            if(isinstance(instruccion, Asignacion)):
                if(self.ts.getSymbol(instruccion.id.id, instruccion.typeExp)==None):
                    self.ts.newSymbol(
                        Symbol(
                            pos, 
                            instruccion.id.id, 
                            TYPE.NOTHING,
                            scope,
                            instruccion.id.row,
                            instruccion.id.col,
                            None
                        )
                    )
                    pos += 1
    
    def conditionError(self, main):
        lv = main.getLabel()
        lf = main.getLabel()
        return ValueC3D(
            LogicC3D(
                [lv], 
                [lf]
            ), 
            TYPE.BOOL, 
            [
                InstruccionC3D(lf, None, None, None, None, TYPE.GOTO),
                InstruccionC3D(lv, None, None, None, None, TYPE.GOTO)
            ]
        )
    
    def translate(self, main, ts, scope):
        nscope = f'{scope}_WHILE'
        translation = []
        labels = []
        conditionc3d = self.condition.translate(main, ts, scope)
        if(conditionc3d.type != TYPE.BOOL):
            conditionc3d = self.conditionError(main)
        insc3d = []
        self.ts = SymbolTable(ts)
        self.getSymbols(nscope)
        for instruction in self.instructions:
            res = instruction.translate(main, self.ts, nscope)
            insc3d += res
        ll = main.getLabel()
        translation.append(InstruccionC3D(ll, None, None, None, None, TYPE.LABEL))
        translation += conditionc3d.c3d
        for label in conditionc3d.tmp.lv:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        translation += insc3d
        translation.append(InstruccionC3D(ll, None, None, None, None, TYPE.GOTO))
        for label in conditionc3d.tmp.lf:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        for label in labels:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        return translation