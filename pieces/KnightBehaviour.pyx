from Array import Array2D, get_l_positions
import numpy as np
cimport numpy as np
from custom_types cimport Piece
from custom_types import Piece


# @profile
cpdef list allowed_moves(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef tuple shape = (board.shape[0], board.shape[1])
    surrounding_positions = get_l_positions(pos, shape)
    filt_all_ms = []
    for move_pos in surrounding_positions:
        mp_piece = board[move_pos[0]][move_pos[1]]
        if not isinstance(mp_piece, Piece):
            filt_all_ms.append(move_pos)
    return filt_all_ms


# @profile
cpdef list allowed_takes(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef tuple shape = (board.shape[0], board.shape[1])
    surrounding_positions = get_l_positions(pos, shape)
    filt_all_ts = []
    for take_pos in surrounding_positions:
        tp_piece = board[take_pos[0]][take_pos[1]]
        if isinstance(tp_piece, Piece):
            if tp_piece.is_white != piece.is_white:
                filt_all_ts.append(take_pos)
    return filt_all_ts
