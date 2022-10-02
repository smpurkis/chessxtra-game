from ast import Set, Tuple
import importlib
from typing import Dict
from Array import Array2D, check_position_is_on_board

Position = Tuple

PIECE_CODES = {"KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"}
PIECE_CODES_SYMBOL = {}


def get_piece_code_dict() -> Dict[str, str]:
    piece_code_dict = {}
    for piece_code in PIECE_CODES:
        piece_code_dict[piece_code] = piece_code
        piece_code_dict[piece_code.lower()] = piece_code
        index = 0
        if piece_code == "KNIGHT":
            index += 1
        piece_code_dict[piece_code[index]] = piece_code
        piece_code_dict[piece_code[index].lower()] = piece_code
    return piece_code_dict


PIECE_CODE_DICT = get_piece_code_dict()
ALLOWED_PIECE_CODES = PIECE_CODE_DICT.keys()


class PieceNotAllowed(Exception):
    pass


class Piece:
    def __init__(self, position: Position, symbol: str) -> None:
        self.position = position
        if symbol not in ALLOWED_PIECE_CODES:
            raise PieceNotAllowed(
                f"Piece '{symbol}' not allowed, please choose from {ALLOWED_PIECE_CODES}"
            )
        self.symbol = symbol
        self.full_symbol = PIECE_CODE_DICT[self.symbol]
        self.is_white = symbol.isupper()
        self.colour = "white" if self.is_white else "black"
        self.in_play = True
        self.has_moved = False
        behaviour_import = f"{self.full_symbol.lower().capitalize()}Behaviour"
        self.behaviour = getattr(
            importlib.import_module(f"pieces.{behaviour_import}"), behaviour_import
        )

    def __str__(self) -> str:
        return self.symbol

    def __repr__(self) -> str:
        return f"{self.colour.capitalize()} {self.full_symbol.lower().capitalize()} {self.position}"

    def get_legal_moves(self, board: Array2D):
        return self.allowed_moves(board).union(self.allowed_takes(board))

    def allowed_moves(self, board: Array2D):
        pos = self.position
        new_positions = self.behaviour.allowed_moves(self, board, pos, self.is_white)
        new_positions = {
            p for p in new_positions if check_position_is_on_board(p, board.shape)
        }
        return new_positions

    def allowed_takes(self, board: Array2D):
        pos = self.position
        new_positions = self.behaviour.allowed_takes(self, board, pos, self.is_white)
        new_positions = {
            p for p in new_positions if check_position_is_on_board(p, board.shape)
        }
        return new_positions

    def update_position(self, position: Position):
        self.position = position


if __name__ == "__main__":
    p = Piece(position=(0, 4), symbol="P")
    print(p)
    print(p.allowed_moves())
    print(p.allowed_takes())
