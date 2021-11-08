from classes.InstruccionC3D import InstruccionC3D
from classes.Value import Value
from classes.Tipo import TYPE
class Print:
    def __init__(self, val, type, row, col):
        self.val = val
        self.type = type
        self.row = row
        self.col = col
    
    def translate(self, main, ts):
        translation = []
        for element in main.imports:
            if(element == "fmt"):
                break
        else:
            main.imports.append("fmt")
        for value in self.val:
            res = value.translate(main, ts)
            if(res.type == TYPE.INT64 or res.type == TYPE.FLOAT64 or res.type == TYPE.CHAR):
                translation += res.c3d
                translation.append(InstruccionC3D(None, None, res.tmp, None, res.type, TYPE.PRINT))
            elif(res.type == TYPE.STRING):
                translation += res.c3d
                if(main.functions.get('printString')==None):
                    main.addPrint()
                tmp = main.getTemp()
                tmp2 = main.getTemp()
                pos = ts.getLength()
                translation += [
                    InstruccionC3D(tmp, None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D(tmp2, None, tmp, None, 0, TYPE.ADDITION),
                    InstruccionC3D('stack', tmp, res.tmp, None, None, TYPE.ASSIGN),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.ADDITION),
                    InstruccionC3D('printString', None, None, None, None, TYPE.CALL),
                    InstruccionC3D('P', None, 'P', None, pos, TYPE.SUBSTRACTION),
                ]
            elif(res.type == TYPE.BOOL):
                lv = main.getLabel()
                lf = main.getLabel()
                ls = main.getLabel()
                if(res.tmp != 0):
                    translation.append(InstruccionC3D(lv, None, None, None, None, TYPE.GOTO))
                    translation.append(InstruccionC3D(lf, None, None, None, None, TYPE.GOTO))
                else:
                    translation.append(InstruccionC3D(lf, None, None, None, None, TYPE.GOTO))
                    translation.append(InstruccionC3D(lv, None, None, None, None, TYPE.GOTO))
                translation += [
                    InstruccionC3D(lv, None, None, None, None, TYPE.LABEL),
                    InstruccionC3D(None, None, 116, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 114, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 117, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 101, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(ls, None, None, None, None, TYPE.GOTO),
                    InstruccionC3D(lf, None, None, None, None, TYPE.LABEL),
                    InstruccionC3D(None, None, 102, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 97, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 108, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 115, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(None, None, 101, None, TYPE.CHAR, TYPE.PRINT),
                    InstruccionC3D(ls, None, None, None, None, TYPE.LABEL),
                ]
            if(self.type == TYPE.PRINTLN):
                translation.append(InstruccionC3D(None, None, 10, None, TYPE.CHAR, TYPE.PRINT ))
        return translation
                
            
