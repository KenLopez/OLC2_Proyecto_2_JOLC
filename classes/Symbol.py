class Symbol:
    def __init__(self, id, type, scope, row, col):
        self.id = id
        self.type = type
        self.scope = scope
        self.row = row
        self.col = col