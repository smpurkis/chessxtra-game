from typing import List

from Array import Array2D, get_col_row_positions, sort_by_distance
from pieces.Piece import Piece, Position


# @profile
def allowed_moves(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
    index = -1 if is_white else 1
    col_row_positions = get_col_row_positions(pos, board.shape)
    filt_all_ms = []
    for positions in col_row_positions:
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
def allowed_takes(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
    index = -1 if is_white else 1
    col_row_positions = get_col_row_positions(pos, board.shape)
    filt_all_ts = []
    for positions in col_row_positions:
        for dir_positions in positions:
            dir_positions = sort_by_distance(piece.position, dir_positions)
            for take_pos in dir_positions:
                tp_piece = board[take_pos[0]][take_pos[1]]
                if isinstance(tp_piece, Piece):
                    if tp_piece.is_white != piece.is_white:
                        filt_all_ts.append(take_pos)
                    break
    return filt_all_ts
