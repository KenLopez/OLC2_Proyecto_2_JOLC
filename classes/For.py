from classes.InstruccionC3D import InstruccionC3D
from classes.LogicC3D import LogicC3D
from classes.Value import Value
from classes.Symbol import Symbol
from classes.ValueC3D import ValueC3D
from classes.Variable import Variable
from classes.Asignacion import Asignacion
from classes.Tipo import TYPE
from classes.SymbolTable import SymbolTable
class For:
    def __init__(self, variable, range, instrucciones, row, col):
        self.variable = variable
        self.range = range
        self.instrucciones = instrucciones
        self.row = row
        self.col = col
    
    def getSymbols(self, scope):
        pos = self.ts.getLength()
        for instruccion in self.instrucciones:
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
    
    def translate(self, main, ts, scope):
        nscope = f'{scope}_FOR'
        pos = ts.getLength()
        translation = []
        ls = []
        ll = []
        insc3d = []
        controls = []
        r = self.range.translate(main, ts, scope)
        t = TYPE.INT64
        if(r.type == TYPE.STRING):
            if(main.functions.get('stringLength')==None):
                main.addStringLength()
            t = TYPE.STRING
            inc = main.getTemp()
            end = -1
            cmp = TYPE.EQUAL
        if(r.type == TYPE.RANGE):
            t = TYPE.INT64
            inc = r.tmp[0]
            end = r.tmp[1]
            cmp = TYPE.GREATER
        elif(r.type == TYPE.LIST):
            t = TYPE.LIST
        else:
            pass    
        nts = SymbolTable(ts)
        nts.newSymbol(Symbol(pos, self.variable, t, nscope, self.row, self.col, None))
        self.ts = SymbolTable(nts)
        self.getSymbols(nscope)
        for instruction in self.instrucciones:
            res = instruction.translate(main, self.ts, nscope)
            if(isinstance(res, ValueC3D)):
                insc3d += res.c3d
                for control in res.tmp:
                    if(control.type == TYPE.CONTINUE):
                        ll.append(control.label)
                    elif(control.type == TYPE.BREAK):
                        if(str(scope).__contains__('FOR') or str(scope).__contains__('WHILE')):
                            controls.append(control)
                        else:
                            ls.append(control.label)
            else:
                insc3d += res
        if(r.type==TYPE.STRING):
            tmps = [main.getTemp(), main.getTemp(), main.getTemp(), main.getTemp()]
            labels = [main.getLabel(), main.getLabel(), main.getLabel()]
            translation += r.c3d
            translation += [
                InstruccionC3D(inc, None, 0, None, None, TYPE.ASSIGN),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(tmps[0], None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D(tmps[1], None, r.tmp, None, inc, TYPE.ADDITION),
                InstruccionC3D(tmps[2], None, 'heap', tmps[1], None, TYPE.ASSIGN),
                InstruccionC3D(tmps[3], None, 'H', None, None, TYPE.ASSIGN),
                InstruccionC3D('heap', 'H', tmps[2], None, None, TYPE.ASSIGN),
                InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
                InstruccionC3D('heap', 'H', -1, None, None, TYPE.ASSIGN),
                InstruccionC3D('H', None, 'H', None, 1, TYPE.ADDITION),
                InstruccionC3D('stack', tmps[0], tmps[3], None, None, TYPE.ASSIGN),
                InstruccionC3D(labels[1], None, tmps[2], None, end, cmp),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
            ]
            translation += insc3d
            for label in ll:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation += [
                InstruccionC3D(inc, None, inc, None, 1, TYPE.ADDITION),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            ]
        elif(r.type==TYPE.RANGE):
            tmps = [main.getTemp(), main.getTemp(), main.getTemp()]
            labels = [main.getLabel(), main.getLabel(), main.getLabel()]
            translation += r.c3d
            translation += [
                InstruccionC3D(tmps[0], None, inc, None, None, TYPE.ASSIGN),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.LABEL),
                InstruccionC3D(tmps[1], None, 'P', None, pos, TYPE.ADDITION),
                InstruccionC3D('stack', tmps[1], tmps[0], None, None, TYPE.ASSIGN),
                InstruccionC3D(labels[1], None, tmps[0], None, end, cmp),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[0], None, None, None, None, TYPE.LABEL),
            ]
            translation += insc3d
            for label in ll:
                translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
            translation += [
                InstruccionC3D(tmps[0], None, tmps[0], None, 1, TYPE.ADDITION),
                InstruccionC3D(labels[2], None, None, None, None, TYPE.GOTO),
                InstruccionC3D(labels[1], None, None, None, None, TYPE.LABEL),
            ]
        for label in ls:
            translation.append(InstruccionC3D(label, None, None, None, None, TYPE.LABEL))
        if(len(controls)>0):
            translation = ValueC3D(controls, TYPE.CONTROL, translation)
        return translation
        