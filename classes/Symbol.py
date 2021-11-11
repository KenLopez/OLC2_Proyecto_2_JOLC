class Symbol:
    def __init__(self, pos, id, type, scope, row, col, ext):
        self.pos = pos
        self.id = id
        self.type = type
        self.scope = scope
        self.row = row
        self.col = col
        self.ext = ext