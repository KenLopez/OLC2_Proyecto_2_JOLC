from classes.Tipo import TYPE
class InstruccionC3D:
    def __init__(self, asignacion, access, op1, opAccess, op2, funcion):
        self.asignacion = asignacion
        self.op1 = op1
        self.op2 = op2
        self.funcion = funcion
        self.access = access
        self.opAccess = opAccess

    def translate(self):
        if(self.funcion == TYPE.LABEL):
            return f'{self.asignacion}:\n'
        if(self.funcion == TYPE.GOTO):
            return f'goto {self.asignacion};\n'
        if(self.funcion == TYPE.PRINT):
            if(self.op2 == TYPE.CHAR):
                return f'fmt.Printf("%c", int({self.op1}));\n'
            if(self.op2 == TYPE.INT64):
                return f'fmt.Printf("%d", int({self.op1}));\n'
            if(self.op2 == TYPE.FLOAT64):
                return f'fmt.Printf("%f", {self.op1});\n'
        if(self.funcion == TYPE.ADDITION):
            return f'{self.asignacion} = {self.op1} + {self.op2};\n'
        if(self.funcion == TYPE.SUBSTRACTION):
            return f'{self.asignacion} = {self.op1} - {self.op2};\n'
        if(self.funcion == TYPE.MULTIPLICATION):
            return f'{self.asignacion} = {self.op1} * {self.op2};\n'
        if(self.funcion == TYPE.DIVISION):
            return f'{self.asignacion} = {self.op1} / {self.op2};\n'
        if(self.funcion == TYPE.MODULUS):
            return f'{self.asignacion} = math.Mod({self.op1}, {self.op2});\n'
        if(self.funcion == TYPE.ASSIGN):
            if(self.access != None):
                return f'{self.asignacion}[int({self.access})] = {self.op1};\n'
            if(self.opAccess != None):
                return f'{self.asignacion} = {self.op1}[int({self.opAccess})];\n'
            return f'{self.asignacion} = {self.op1};\n'
        if(self.funcion == TYPE.EQUAL):
            return f'if {self.op1} == {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.DIFFERENT):
            return f'if {self.op1} != {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.GREATER):
            return f'if {self.op1} > {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.GREATEREQUAL):
            return f'if {self.op1} >= {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.LOWEREQUAL):
            return f'if {self.op1} <= {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.LOWER):
            return f'if {self.op1} < {self.op2} {{goto {self.asignacion};}}\n'
        if(self.funcion == TYPE.CALL):
            return f'{self.asignacion}();\n'
        if(self.funcion == TYPE.RETURN):
            return f'return;\n'