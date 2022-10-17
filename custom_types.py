from dataclasses import dataclass
from typing import Tuple

Position = Tuple[int, int]


@dataclass(unsafe_hash=True)
class Piece:
    position: Position
    symbol: str
    full_symbol: str
    is_white: bool
    colour: str
    in_play: bool
    has_moved: bool
