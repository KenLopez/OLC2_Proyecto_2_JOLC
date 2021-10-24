from classes.StructAccess import StructAccess
from classes.ArrayAccess import ArrayAccess
from classes.Value import Value
from classes.Symbol import Symbol
from classes.Tipo import TYPE
class Asignacion:
    def __init__(self, id, val, type, typeExp, row, col):
        self.id = id
        self.val = val
        self.type = type
        self.typeExp = typeExp
        self.row = row
        self.col = col
    
    def execute(self, main, tabla, scope):
        val = self.val
        if(self.val != None):
            val = self.val.execute(main, tabla, scope)
        if(val==TYPE.ERROR):
            return TYPE.ERROR
        if(self.type == TYPE.ANY):
            if(isinstance(self.id, ArrayAccess)):
                res = self.id.get(main, tabla, scope)
                if(res == TYPE.ERROR):
                    return TYPE.ERROR
                res.type = val.type
                res.val = val.val
                if(isinstance(res, Value) and isinstance(val.val, Value)):
                        res.typeStruct = val.val.typeStruct
            elif(isinstance(self.id, StructAccess)):
                res = self.id.get(main, tabla, scope)
                if(res == TYPE.ERROR):
                    return TYPE.ERROR
                res.type = val.type
                res.val = val.val
                if(isinstance(res, Value) and isinstance(val.val, Value)):
                        res.typeStruct = val.val.typeStruct
            else:
                tabla.updateSymbol(Symbol(self.id, val, scope, self.row, self.col), self.typeExp)
            return Value(None, TYPE.NOTHING, self.row, self.col)
        elif(self.type == val.type or (val.type == TYPE.STRUCT and val.typeStruct == self.type)):
            if(isinstance(self.id, ArrayAccess)):
                res = self.id.get(main, tabla, scope)
                if(res == TYPE.ERROR):
                    return TYPE.ERROR
                res.type = val.type
                res.val = val.val
                if(isinstance(res, Value) and isinstance(val.val, Value)):
                        res.typeStruct = val.val.typeStruct
            elif(isinstance(self.id, StructAccess)):
                res = self.id.get(main, tabla, scope)
                if(res == TYPE.ERROR):
                    return TYPE.ERROR
                res.type = val.type
                res.val = val.val
                if(isinstance(res, Value) and isinstance(val.val, Value)):
                        res.typeStruct = val.val.typeStruct
            else:
                tabla.updateSymbol(Symbol(self.id, val, scope, self.row, self.col), self.typeExp)
            return Value(None, TYPE.NOTHING, self.row, self.col)
        else:
            return TYPE.ERROR
