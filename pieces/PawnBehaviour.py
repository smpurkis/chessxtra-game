from typing import List

from Array import Array2D, check_position_is_on_board
from pieces.Piece import Piece, Position


# @profile
def allowed_moves(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
    index = -1 if is_white else 1
    new_positions = [(pos[0] + index, pos[1])]
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    ]
    filt_all_ms = []
    for move_pos in new_positions:
        mp_piece = board[move_pos[0]][move_pos[1]]
        if not isinstance(mp_piece, Piece):
            filt_all_ms.append(move_pos)
    return filt_all_ms


# @profile
def allowed_takes(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
    index = -1 if is_white else 1
    new_positions = [(pos[0] + index, pos[1] + row_i) for row_i in (-1, 1)]
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    ]
    filt_all_ts = []
    for take_pos in new_positions:
        tp_piece = board[take_pos[0]][take_pos[1]]
        if isinstance(tp_piece, Piece):
            if tp_piece.is_white != piece.is_white:
                filt_all_ts.append(take_pos)
    return filt_all_ts