from classes.Tipo import TYPE
class InstruccionC3D:
    def __init__(self, asignacion, op1, op2, funcion, access=None):
        self.asignacion = asignacion
        self.op1 = op1
        self.op2 = op2
        self.funcion = funcion
        self.access = access