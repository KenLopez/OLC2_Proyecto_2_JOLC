from classes.Tipo import TYPE


class Funcion:
    def __init__(self, params, instructions, type):
        self.params = params
        self.instructions = instructions
        self.type = type     
    
    def translate(self, main, ts, scope):
        pass
