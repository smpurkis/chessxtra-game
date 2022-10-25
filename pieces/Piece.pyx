cimport cython

from Array import check_position_is_on_board
import numpy as np
cimport numpy as np
from custom_types cimport Piece
from custom_types import Piece
from pieces import (BishopBehaviour, KingBehaviour, KnightBehaviour,
                    PawnBehaviour, QueenBehaviour, RookBehaviour)

PIECE_CODES = {"KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"}

Position = tuple

cpdef tuple get_piece_code_dict():
    piece_code_dict = {}
    inverse_piece_code_dict = {}
    for piece_code in PIECE_CODES:
        piece_code_dict[piece_code] = piece_code
        piece_code_dict[piece_code.lower()] = piece_code
        index = 0
        if piece_code == "KNIGHT":
            index += 1
        piece_code_dict[piece_code[index]] = piece_code
        piece_code_dict[piece_code[index].lower()] = piece_code

        inverse_piece_code_dict[piece_code] = [
            piece_code,
            piece_code.lower(),
            piece_code[index],
            piece_code[index].lower(),
        ]
    return piece_code_dict, inverse_piece_code_dict


PIECE_CODE_DICT, INVERSE_PIECE_CODE_DICT = get_piece_code_dict()
ALLOWED_PIECE_CODES = PIECE_CODE_DICT.keys()


class PieceNotAllowed(Exception):
    pass


cpdef Piece make_piece(tuple position, str symbol):
    piece = Piece(
        position=position,
        symbol=symbol,
        full_symbol=PIECE_CODE_DICT[symbol],
        is_white=symbol.isupper(),
        colour="white" if symbol.isupper() else "black",
        in_play=True,
        has_moved=False
    )
    return piece


cpdef list allowed_moves(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef:
        str full_symbol
        list allowed_moves_list

    full_symbol = piece.full_symbol
    if full_symbol == "KING":
        allowed_moves_list = KingBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "QUEEN":
        allowed_moves_list = QueenBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "ROOK":
        allowed_moves_list = RookBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "BISHOP":
        allowed_moves_list = BishopBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "KNIGHT":
        allowed_moves_list = KnightBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "PAWN":
        allowed_moves_list = PawnBehaviour.allowed_moves(piece, board, pos, is_white)
    else:
        allowed_moves_list = []
    return allowed_moves_list


cpdef list get_allowed_moves(Piece piece, np.ndarray board):
    cdef:
        tuple pos
        list new_positions

    pos = piece.position
    new_positions = allowed_moves(piece, board, pos, piece.is_white)
    cdef tuple shape = (board.shape[0], board.shape[1])
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, shape)
    ]
    return new_positions


cpdef list allowed_takes(
    Piece piece, np.ndarray board, tuple pos, bint is_white
):
    cdef:
        str full_symbol
        list allowed_moves_list

    full_symbol = piece.full_symbol
    if full_symbol == "KING":
        allowed_takes_list = KingBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "QUEEN":
        allowed_takes_list = QueenBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "ROOK":
        allowed_takes_list = RookBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "BISHOP":
        allowed_takes_list = BishopBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "KNIGHT":
        allowed_takes_list = KnightBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "PAWN":
        allowed_takes_list = PawnBehaviour.allowed_takes(piece, board, pos, is_white)
    else:
        allowed_takes_list = []
    return allowed_takes_list


# @profile
cpdef list get_allowed_takes(Piece piece, np.ndarray board):
    cdef: 
        tuple pos
        list new_positions

    pos = piece.position
    new_positions = allowed_takes(piece, board, pos, piece.is_white)
    cdef tuple shape = (board.shape[0], board.shape[1])
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, shape)
    ]
    return new_positions


cpdef list get_legal_moves(Piece piece, np.ndarray board):
    cdef:
        list allowed_moves
        list allowed_takes

    allowed_moves = get_allowed_moves(piece, board)
    allowed_takes = get_allowed_takes(piece, board)
    allowed = list(set(allowed_moves + allowed_takes))
    return allowed
