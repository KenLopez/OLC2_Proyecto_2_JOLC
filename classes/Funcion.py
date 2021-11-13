from classes.Asignacion import Asignacion
from classes.InstruccionC3D import InstruccionC3D
from classes.Symbol import Symbol
from classes.SymbolTable import SymbolTable
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D


class Funcion:
    def __init__(self, params, instructions, type):
        self.params = params
        self.instructions = instructions
        self.type = type
        self.ts = SymbolTable(None)
    
    def getSymbols(self, scope):
        for param in self.params:
            if(param.type.val == TYPE.LIST):
                ext = param.type.type
            else:
                ext = None
            self.ts.newSymbol(
                Symbol(
                    len(self.ts.symbols), 
                    param.id, 
                    param.type.val,
                    scope,
                    0,
                    0,
                    ext
                )
            )
        pos = len(self.ts.symbols)
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
        if(self.type.val == TYPE.LIST):
            ext = self.type.type
        else:
            ext = None
        self.ts.newSymbol(
            Symbol(
                pos,
                '#',
                self.type.val,
                scope,
                0,
                0,
                ext
            )
        )
    
    def translate(self, main, ts, id):
        scope = f'FUNCTION_{id}'
        translation = []
        ls = []
        for instruction in self.instructions:
            res = instruction.translate(main, self.ts, scope)
            if(isinstance(res, ValueC3D)):
                if(res.type == TYPE.CONTROL):
                    for c in res.tmp:
                        ls.append(c.label)
                translation += res.c3d
            else:
                translation += res
        for label in ls:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        translation.append(InstruccionC3D(None, None, None, None, None, TYPE.RETURN))
        return translation
