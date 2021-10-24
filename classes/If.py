from classes.SymbolTable import SymbolTable
from classes.Value import Value
from classes.Tipo import TYPE
class If:
    def __init__(self, conditions, instructions, elseinstructions, row, col):
        self.conditions = conditions
        self.instructions = instructions
        self.elseinstructions = elseinstructions
        self.row = row
        self.col = col
    
    def execute(self, main, tabla, scope):
        nscope = scope+"_IF"
        ntabla = SymbolTable(tabla)
        for i in range(len(self.conditions)):
            res = self.conditions[i].execute(main, ntabla, nscope)
            if(res==TYPE.ERROR):
                return TYPE.ERROR
            elif(res.type!=TYPE.TYPEBOOL):
                return TYPE.ERROR
            elif(res.val):
                for j in self.instructions[i]:
                    res2 = j.execute(main, ntabla, nscope)
                    if(res2 == TYPE.ERROR):
                        return TYPE.ERROR
                    if(res2.type == TYPE.CONTINUE or res2.type == TYPE.BREAK or res2.type == TYPE.RETURN):
                        return res2
                return Value(None, TYPE.NOTHING, self.row, self.col)
        for i in self.elseinstructions:
            res = i.execute(main, ntabla, nscope)
            if(res == TYPE.ERROR):
                return TYPE.ERROR
            if(res.type == TYPE.CONTINUE or res.type == TYPE.BREAK or res.type == TYPE.RETURN):
                return res
        return Value(None, TYPE.NOTHING, self.row, self.col)
