from classes.InstruccionC3D import InstruccionC3D
from classes.Value import Value
from classes.Tipo import TYPE
class Print:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col
    
    def translate(self, main):
        translation = []
        for element in main.imports:
            if(element == "fmt"):
                break
        else:
            main.imports.append("fmt")
        for value in self.val:
            res = value.translate(main)
            if(res.type == TYPE.INT64 or res.type == TYPE.FLOAT64 or res.type == TYPE.CHAR):
                translation.append(InstruccionC3D(None, res.tmp, res.type, TYPE.PRINT))
            elif(res.type == TYPE.STRING):
                if(main.functions.get('printString')==None):
                    main.addPrint()
                
            
