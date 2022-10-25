from Array import Array2D, get_diagonal_positions, sort_by_distance
import numpy as np
cimport numpy as np
from custom_types cimport Piece
from custom_types import Piece

# @profile
cpdef list allowed_moves(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef:
        tuple shape = (board.shape[0], board.shape[1])
        list diagonal_positions
        list filt_all_ms
        list positions
        list dir_positions
        tuple move_pos

    diagonal_positions = get_diagonal_positions(pos, shape)
    filt_all_ms = []
    for positions in diagonal_positions:
        for dir_positions in positions:
            dir_positions = sort_by_distance(piece.position, dir_positions)
            for move_pos in dir_positions:
                mp_piece = board[move_pos[0]][move_pos[1]]
                if isinstance(mp_piece, Piece):
                    break
                else:
                    filt_all_ms.append(move_pos)
    return filt_all_ms


# @profile
cpdef list allowed_takes(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef:
        tuple shape = (board.shape[0], board.shape[1])
        list diagonal_positions
        list filt_all_ts
        list positions
        list dir_positions
        tuple take_pos
    
    diagonal_positions = get_diagonal_positions(pos, shape)
    filt_all_ts = []
    for positions in diagonal_positions:
        for dir_positions in positions:
            dir_positions = sort_by_distance(piece.position, dir_positions)
            for take_pos in dir_positions:
                tp_piece = board[take_pos[0]][take_pos[1]]
                if isinstance(tp_piece, Piece):
                    if tp_piece.is_white != piece.is_white:
                        filt_all_ts.append(take_pos)
                    break
    return filt_all_ts
