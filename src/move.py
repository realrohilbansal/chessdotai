class Move():
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    def __str__(self):
        s = ''
        s += f'({self.initial}) -> ({self.final})'
        return s
    
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
