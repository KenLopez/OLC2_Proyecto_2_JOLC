from classes.InstruccionC3D import InstruccionC3D
from classes.Value import Value
from classes.Tipo import TYPE
from classes.ValueC3D import ValueC3D

class Aritmetica:

    def __init__(self, expIzq, expDer, type, row, col):
        self.expIzq = expIzq
        self.expDer = expDer
        self.type = type
        self.row = row
        self.col = col
    
    def checkTypes(self, der, izq):
        if(
            self.type == TYPE.ADDITION 
            or self.type == TYPE.SUBSTRACTION 
            or self.type == TYPE.MODULUS
            or self.type == TYPE.DIVISION
        ):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
                elif(der.type == TYPE.INT64):
                    return TYPE.INT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.FLOAT64 or der.type == TYPE.INT64):
                    return TYPE.FLOAT64
        elif(self.type == TYPE.MULTIPLICATION):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.INT64):
                    return TYPE.INT64
                elif(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.FLOAT64 or der.type == TYPE.INT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.STRING and der.type == TYPE.STRING):
                return TYPE.STRING
        elif(self.type == TYPE.POWER):
            if(izq.type == TYPE.INT64):
                if(der.type == TYPE.INT64):
                    return TYPE.INT64
                elif(der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.FLOAT64):
                if(der.type == TYPE.INT64 or der.type == TYPE.FLOAT64):
                    return TYPE.FLOAT64
            elif(izq.type == TYPE.STRING and der.type == TYPE.INT64):
                return TYPE.STRING
        return TYPE.ERROR
    
    def translate(self, main):
        der  = self.expDer.translate(main) 
        izq = self.expIzq.translate(main)
        translation = ValueC3D(0, self.checkTypes())
        if(translation.type == TYPE.ERROR): 
            return translation
        translation.tmp = main.getTemp()
        translation.c3d.extend(izq.c3d)
        translation.c3d.extend(der.c3d)
        if(translation.type == TYPE.INT64 or translation.type == TYPE.FLOAT64):
            if(self.type == TYPE.MODULUS):
               pass 
            translation.c3d.append(InstruccionC3D(translation.tmp, izq.tmp, der.tmp, self.type))
        else:
            if(self.type == TYPE.ADDITION):
                translation.c3d.append(InstruccionC3D(translation.tmp, 'heap', 'H', TYPE.LIST))
            
            
        
                    