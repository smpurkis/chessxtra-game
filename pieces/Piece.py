from typing import Dict, Tuple, List

from Array import Array2D, check_position_is_on_board
from custom_types import Piece, Position
from pieces import (
    BishopBehaviour,
    KingBehaviour,
    KnightBehaviour,
    PawnBehaviour,
    QueenBehaviour,
    RookBehaviour,
)

PIECE_CODES = {"KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"}


# @profile
def get_piece_code_dict() -> Tuple[Dict[str, str], Dict[str, List[str]]]:
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


# @profile
def make_piece(position: Position, symbol: str) -> Piece:
    return Piece(
        position=position,
        symbol=symbol,
        full_symbol=PIECE_CODE_DICT[symbol],
        is_white=symbol.isupper(),
        colour="white" if symbol.isupper() else "black",
        in_play=True,
        has_moved=False,
    )


# @profile
def allowed_moves(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
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


# @profile
def get_allowed_moves(piece: Piece, board: Array2D) -> List[Position]:
    pos = piece.position
    new_positions: List[Position] = allowed_moves(piece, board, pos, piece.is_white)
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    ]
    return new_positions


# @profile
def allowed_takes(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> List[Position]:
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
def get_allowed_takes(piece: Piece, board: Array2D) -> List[Position]:
    pos = piece.position
    new_positions: List[Position] = allowed_takes(piece, board, pos, piece.is_white)
    new_positions = [
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    ]
    return new_positions


# @profile
def get_legal_moves(piece: Piece, board: Array2D) -> List[Position]:
    allowed_moves = get_allowed_moves(piece, board)
    allowed_takes = get_allowed_takes(piece, board)
    allowed = list(set(allowed_moves + allowed_takes))
    return allowed
