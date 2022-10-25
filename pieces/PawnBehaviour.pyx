from Array import Array2D, check_position_is_on_board
import numpy as np
cimport numpy as np
from custom_types cimport Piece
from custom_types import Piece


# @profile
cpdef list allowed_moves(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef tuple shape = (board.shape[0], board.shape[1])
    index = -1 if is_white else 1
    new_positions = [(pos[0] + index, pos[1])]
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, shape)
    ]
    filt_all_ms = []
    for move_pos in new_positions:
        mp_piece = board[move_pos[0]][move_pos[1]]
        if not isinstance(mp_piece, Piece):
            filt_all_ms.append(move_pos)
    return filt_all_ms


# @profile
cpdef list allowed_takes(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef tuple shape = (board.shape[0], board.shape[1])
    index = -1 if is_white else 1
    new_positions = [(pos[0] + index, pos[1] + row_i) for row_i in (-1, 1)]
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, shape)
    ]
    filt_all_ts = []
    for take_pos in new_positions:
        tp_piece = board[take_pos[0]][take_pos[1]]
        if isinstance(tp_piece, Piece):
            if tp_piece.is_white != piece.is_white:
                filt_all_ts.append(take_pos)
    return filt_all_ts
