from classes.Value import Value
from classes.Tipo import TYPE

class SymbolTable:
    def __init__(self, padre):
        self.padre = padre
        self.symbols = {}

    def newSymbol(self, symbol, type):
        s = self.getSymbol(symbol.id, type)
        if(s == TYPE.ERROR):
            self.symbols[symbol.id] = symbol
        else:
            return TYPE.ERROR
        return Value(None, TYPE.NOTHING, symbol.row, symbol.col)
    
    def newSymbol(self, symbol):
        self.symbols[symbol.id] = symbol
    
    def updateSymbol(self, symbol, type):
        s = self.getSymbol(symbol, type)
        s.type = symbol.type

    def getSymbol(self, id, type):
        s = self.symbols.get(id)
        if(type == TYPE.GLOBAL):
            if(self.padre == None):
                return s
            else:
                return self.padre.getSymbol(id, type)
        if(type == TYPE.LOCAL):
            return s
        if(s != None):
            return s
        if(self.padre == None):
            return s
        return self.padre.getSymbol(id, type)
    
    def getLength(self):
        l = len(self.symbols)
        if(self.padre != None):
           l = l + self.padre.getLength()
        return l 
