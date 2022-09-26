from pieces.Piece import Position
from Array import Array2D


class RookBehaviour:
    @staticmethod
    def allowed_moves(board: Array2D, pos: Position, is_white: bool) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions

    @staticmethod
    def allowed_takes(board: Array2D, pos: Position, is_white: bool) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions