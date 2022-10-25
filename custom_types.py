from dataclasses import dataclass

Position = tuple

class Piece(object):
    def __init__(self, position: tuple, symbol: str, full_symbol: str, is_white: bool, colour: str, in_play: bool, has_moved: bool):
        self.position = position
        self.symbol = symbol
        self.full_symbol = full_symbol
        self.is_white = is_white
        self.colour = colour
        self.in_play = in_play
        self.has_moved = has_moved

class Game(object):
    def __init__(self, board: Array2D, moves: list, completed: bint, winner: str, turn: str, setup: str, shape: tuple, board_state: Optional[str]):
        self.board = board
        self.moves = moves
        self.completed = completed
        self.winner = winner
        self.turn = turn
        self.setup = setup
        self.shape = shape
        self.board_state = board_state