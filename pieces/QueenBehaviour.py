from turtle import position
from typing import Set
from pieces.Piece import Piece, Position
from Array import (
    Array2D,
    sort_by_distance,
    get_col_row_positions,
    get_diagonal_positions,
)


class QueenBehaviour:
    @staticmethod
    def allowed_moves(
        piece: Piece, board: Array2D, pos: Position, is_white: bool
    ) -> set[Position]:
        position_lines = [
            *get_col_row_positions(pos, board.shape),
            *get_diagonal_positions(pos, board.shape),
        ]
        filt_all_ms = set()
        for positions in position_lines:
            for dir_positions in positions:
                dir_positions = sort_by_distance(piece.position, dir_positions)
                for move_pos in dir_positions:
                    mp_piece = board[move_pos[0]][move_pos[1]]
                    if isinstance(mp_piece, Piece):
                        break
                    else:
                        filt_all_ms.add(move_pos)
        return filt_all_ms

    @staticmethod
    def allowed_takes(
        piece: Piece, board: Array2D, pos: Position, is_white: bool
    ) -> Set[Position]:
        position_lines = [
            *get_col_row_positions(pos, board.shape),
            *get_diagonal_positions(pos, board.shape),
        ]
        filt_all_ts = set()
        for positions in position_lines:
            for dir_positions in positions:
                dir_positions = sort_by_distance(piece.position, dir_positions)
                for take_pos in dir_positions:
                    tp_piece = board[take_pos[0]][take_pos[1]]
                    if isinstance(tp_piece, Piece):
                        if tp_piece.is_white != piece.is_white:
                            filt_all_ts.add(take_pos)
                        break
        return filt_all_ts
