class Square:
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash(tuple(sorted(self.__dict__.items())))

    def has_piece(self):
        return self.piece != None
    
    def is_empty(self):
        return not self.has_piece()

    def has_teampiece(self, color):
        return self.has_piece() and self.piece.color == color
    
    def has_rivalpiece(self, color):
        return self.has_piece() and self.piece.color != color
    
    def isempty_or_rival(self, color):
        return self.is_empty() or self.has_rivalpiece(color) == True
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if  0 > arg or arg > 7:
                return False
        return True 