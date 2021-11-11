from classes.Asignacion import Asignacion
from classes.InstruccionC3D import InstruccionC3D
from classes.Symbol import Symbol
from classes.SymbolTable import SymbolTable
from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D
from classes.LogicC3D import LogicC3D
class If:
    def __init__(self, conditions, instructions, elseinstructions, row, col):
        self.conditions = conditions
        self.instructions = instructions
        self.elseinstructions = elseinstructions
        self.row = row
        self.col = col
        self.ts = None
    
    def getSymbols(self, scope, instrucciones):
        pos = self.ts.getLength()
        for instruccion in instrucciones:
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
        nscope = f'{scope}_IF'
        translation = []
        labels = []
        controls = []
        for i in range(0, len(self.conditions)):
            b = self.conditions[i].translate(main, ts, nscope)
            if(b.type != TYPE.BOOL):
                b = self.conditionError(main)
            translation += b.c3d
            for label in b.tmp.lv:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            self.ts = SymbolTable(ts)
            self.getSymbols(nscope, self.instructions[i])
            for instruction in self.instructions[i]:
                res = instruction.translate(main, self.ts, nscope)
                if(isinstance(res, ValueC3D)):
                    controls += res.tmp
                    translation += res.c3d
                else:
                    translation += res
            ls = main.getLabel()
            translation.append(InstruccionC3D(ls, None, None, None, None, TYPE.GOTO))
            labels.append(ls)
            for label in b.tmp.lf:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        if(len(self.elseinstructions)>0):
            self.ts = SymbolTable(ts)
            self.getSymbols(nscope, self.elseinstructions)
            for instruction in self.elseinstructions:
                res = instruction.translate(main, self.ts, nscope)
                if(isinstance(res, ValueC3D)):
                    controls += res.tmp
                    translation += res.c3d
                else:
                    translation += res
        for label in labels:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        if(len(controls)>0):
            translation = ValueC3D(controls, TYPE.CONTROL, translation)
        return translation

            

