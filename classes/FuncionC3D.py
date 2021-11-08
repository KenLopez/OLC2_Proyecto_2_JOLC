class FuncionC3D:
    def __init__(self, name, c3d):
        self.name = name
        self.c3d = c3d

    def translate(self):
        t = f'''func {self.name}(){{\n'''
        for instruccion in self.c3d:
            t += '\t' + instruccion.translate()
        t += f'}}\n'
        return t