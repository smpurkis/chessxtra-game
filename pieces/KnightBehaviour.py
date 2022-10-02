from typing import Set
from pieces.Piece import Piece, Position
from Array import Array2D, get_l_positions


class KnightBehaviour:
    @staticmethod
    def allowed_moves(
        piece: Piece, board: Array2D, pos: Position, is_white: bool
    ) -> Set[Position]:
        surrounding_positions = get_l_positions(pos, board.shape)
        filt_all_ms = set()
        for move_pos in surrounding_positions:
            mp_piece = board[move_pos[0]][move_pos[1]]
            if not isinstance(mp_piece, Piece):
                filt_all_ms.add(move_pos)
        return filt_all_ms

    @staticmethod
    def allowed_takes(
        piece: Piece, board: Array2D, pos: Position, is_white: bool
    ) -> Set[Position]:
        surrounding_positions = get_l_positions(pos, board.shape)
        filt_all_ts = set()
        for take_pos in surrounding_positions:
            tp_piece = board[take_pos[0]][take_pos[1]]
            if isinstance(tp_piece, Piece):
                if tp_piece.is_white != piece.is_white:
                    filt_all_ts.add(take_pos)
        return filt_all_ts
