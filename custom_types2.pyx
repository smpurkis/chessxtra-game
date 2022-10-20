Position = tuple

class Piece:
    def __init__(self, position: tuple, symbol: str, full_symbol: str, is_white: bool, colour: str, in_play: bool, has_moved: bool):
        self.position = position
        self.symbol = symbol
        self.full_symbol = full_symbol
        self.is_white = is_white
        self.colour = colour
        self.in_play = in_play
        self.has_moved = has_moved