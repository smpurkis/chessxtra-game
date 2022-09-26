import importlib
from Array import Array2D

Position = tuple[int, int]

PIECE_CODES = {"KING", "QUEEN", "ROOK", "BISHOP", "KNIGHT", "PAWN"}
PIECE_CODES_SYMBOL = {}


def get_piece_code_dict() -> dict[str, str]:
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


def check_position_in_board_shape(
    position: Position, board: Array2D
) -> bool:
    return (0 <= position[0] <= board.shape[0] - 1) and (
        0 <= position[1] <= board.shape[1] - 1
    )


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
        behaviour_import = f"{self.full_symbol.lower().capitalize()}Behaviour"
        self.behaviour = getattr(
            importlib.import_module(behaviour_import), behaviour_import
        )

    def __str__(self) -> str:
        return self.symbol

    def allowed_moves(self, board: Array2D) -> set[Position]:
        pos = self.position
        new_positions = self.behaviour.allowed_moves(self.is_white, pos)
        new_positions = {
            p for p in new_positions if check_position_in_board_shape(p, board)
        }
        return new_positions

    def allowed_takes(self, board: Array2D) -> set[Position]:
        pos = self.position
        new_positions = self.behaviour.allowed_takes(self.is_white, pos)
        new_positions = {
            p for p in new_positions if check_position_in_board_shape(p, board)
        }
        return new_positions

    def update_position(self, position: Position):
        self.position = position


if __name__ == "__main__":
    p = Piece(position=(0, 4), symbol="P")
    print(p)
    print(p.allowed_moves())
    print(p.allowed_takes())
