from typing import Dict, Set, Tuple

from Array import Array2D, check_position_is_on_board
from custom_types import Piece, Position
from pieces import (BishopBehaviour, KingBehaviour, KnightBehaviour,
                    PawnBehaviour, QueenBehaviour, RookBehaviour)

PIECE_CODES = {"KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"}


def get_piece_code_dict() -> Tuple[Dict[str, str], Dict[str, Set[str]]]:
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

        inverse_piece_code_dict[piece_code] = {
            piece_code,
            piece_code.lower(),
            piece_code[index],
            piece_code[index].lower(),
        }
    return piece_code_dict, inverse_piece_code_dict


PIECE_CODE_DICT, INVERSE_PIECE_CODE_DICT = get_piece_code_dict()
ALLOWED_PIECE_CODES = PIECE_CODE_DICT.keys()


class PieceNotAllowed(Exception):
    pass


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


def allowed_moves(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> Set[Position]:
    full_symbol = piece.full_symbol
    if full_symbol == "KING":
        allowed_moves_set = KingBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "QUEEN":
        allowed_moves_set = QueenBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "ROOK":
        allowed_moves_set = RookBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "BISHOP":
        allowed_moves_set = BishopBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "KNIGHT":
        allowed_moves_set = KnightBehaviour.allowed_moves(piece, board, pos, is_white)
    elif full_symbol == "PAWN":
        allowed_moves_set = PawnBehaviour.allowed_moves(piece, board, pos, is_white)
    else:
        allowed_moves_set = set()
    return allowed_moves_set


def get_allowed_moves(piece: Piece, board: Array2D) -> Set[Position]:
    pos = piece.position
    new_positions: Set[Position] = allowed_moves(piece, board, pos, piece.is_white)
    new_positions = {
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    }
    return new_positions


def allowed_takes(
    piece: Piece, board: Array2D, pos: Position, is_white: bool
) -> Set[Position]:
    full_symbol = piece.full_symbol
    if full_symbol == "KING":
        allowed_takes_set = KingBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "QUEEN":
        allowed_takes_set = QueenBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "ROOK":
        allowed_takes_set = RookBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "BISHOP":
        allowed_takes_set = BishopBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "KNIGHT":
        allowed_takes_set = KnightBehaviour.allowed_takes(piece, board, pos, is_white)
    elif full_symbol == "PAWN":
        allowed_takes_set = PawnBehaviour.allowed_takes(piece, board, pos, is_white)
    else:
        allowed_takes_set = set()
    return allowed_takes_set


# @profile
def get_allowed_takes(piece: Piece, board: Array2D) -> Set[Position]:
    pos = piece.position
    new_positions: Set[Position] = allowed_takes(piece, board, pos, piece.is_white)
    new_positions = {
        p for p in new_positions if check_position_is_on_board(p, board.shape)
    }
    return new_positions


def get_legal_moves(piece: Piece, board: Array2D) -> Set[Position]:
    return get_allowed_moves(piece, board).union(get_allowed_takes(piece, board))
