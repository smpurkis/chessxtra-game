from pieces.Piece import Position


class RookBehaviour:
    @staticmethod
    def allowed_moves(is_white: bool, pos: Position) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions

    @staticmethod
    def allowed_takes(is_white: bool, pos: Position) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions

    @staticmethod
    def filter_moves(is_white: bool, pos: Position) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions

    @staticmethod
    def filter_takes(is_white: bool, pos: Position) -> list[Position]:
        index = -1 if is_white else 1
        new_positions = [(pos[0] + row_i, pos[1] + index) for row_i in (-1, 1)]
        return new_positions
