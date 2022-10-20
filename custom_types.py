from dataclasses import dataclass

Position = tuple

@dataclass
class Piece:
    position: tuple
    symbol: str
    full_symbol: str
    is_white: bool
    colour: str
    in_play: bool
    has_moved: bool
