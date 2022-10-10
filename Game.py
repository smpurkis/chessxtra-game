from typing import Dict, Set, Tuple, Union, Optional

from Array import Array2D

# import numpy as np
from pieces.Piece import Piece, Position


class IllegalMove(Exception):
    pass


class Game:
    def __init__(
        self,
        shape: Tuple[int, int] = (6, 4),
        setup: str = "rnbk\npppp",
        board_state: Optional[str] = None,
    ) -> None:
        if board_state is not None:
            shape = (len(board_state.split("\n")), len(board_state.split("\n")[0]))
        self.shape = shape
        self.board = Array2D(shape=shape)
        # self.board = np.full(shape=shape, fill_value="-", dtype=object)
        self.moves: list[str] = []
        if board_state is None:
            self.start_setup(setup_position=setup)
        else:
            self.setup(board_state=board_state)
        self.completed = False
        self.winner = ""
        self.turn = "white"

    def check_completed(self) -> None:
        pieces = self.get_pieces()
        white_pieces = {p for p in pieces if p.is_white}
        black_pieces = {p for p in pieces if not p.is_white}
        white_king_exists = (
            len({p for p in white_pieces if p.full_symbol == "KING"}) == 1
        )
        black_king_exists = (
            len({p for p in black_pieces if p.full_symbol == "KING"}) == 1
        )
        if not self.completed:
            if white_king_exists and black_king_exists:
                self.winner = "neither"
            elif not white_king_exists and black_king_exists:
                self.winner = "black"
                self.completed = True
            elif white_king_exists and not black_king_exists:
                self.winner = "white"
                self.completed = True
        else:
            raise Exception("should not get here")

    def setup(self, board_state: str) -> None:
        setup_lines = board_state.split("\n")
        for row_no, lines in enumerate(setup_lines):
            for col_no, piece_code in enumerate(lines):
                if piece_code == "-":
                    self.board[row_no][col_no] = "-"
                else:
                    self.board[row_no][col_no] = Piece((row_no, col_no), piece_code)

    def start_setup(self, setup_position: str) -> None:
        setup_lines = setup_position.split("\n")
        for piece_code, col_no in zip(setup_lines[0], range(self.board.shape[1])):
            self.board[0][col_no] = Piece((0, col_no), piece_code)
            self.board[-1][col_no] = Piece(
                (self.board.shape[0] - 1, col_no), piece_code.upper()
            )

        if len(setup_lines) > 1:
            for piece_code, col_no in zip(setup_lines[1], range(self.board.shape[1])):
                self.board[1][col_no] = Piece((1, col_no), piece_code)
                self.board[-2][col_no] = Piece(
                    (self.board.shape[0] - 2, col_no), piece_code.upper()
                )

    # @profile
    def get_all_legal_moves(
        self, colour: Optional[str] = None, include_empty: bool = True
    ) -> Dict[Piece, Set[Position]]:
        legal_moves = {}
        for row_no in range(self.board.shape[0]):
            for col_no in range(self.board.shape[1]):
                piece: Union[Piece, str] = self.board[row_no][col_no]
                if isinstance(piece, Piece):
                    if colour is None or piece.colour == colour and piece.in_play:
                        piece_legal_moves = piece.get_legal_moves(self.board)
                        if len(piece_legal_moves) > 0 or include_empty:
                            legal_moves[piece] = piece_legal_moves
        return legal_moves

    def get_pieces(self, colour: Optional[str] = None) -> Set[Piece]:
        pieces = set()
        for row_no in range(self.board.shape[0]):
            for col_no in range(self.board.shape[1]):
                piece: Union[Piece, str] = self.board[row_no][col_no]
                if isinstance(piece, Piece):
                    if colour is None or piece.colour == colour and piece.in_play:
                        pieces.add(piece)
        return pieces

    def check_move(self, pos_1: Position, pos_2: Position) -> bool:
        return self.move(pos_1, pos_2, dry_run=True)

    # @profile
    def move(self, pos_1: Position, pos_2: Position, dry_run: bool = False) -> bool:
        piece: Piece = self.board[pos_1[0]][pos_1[1]]

        allowed_moves = piece.allowed_moves(self.board)
        allowed_takes = piece.allowed_takes(self.board)

        if pos_2 not in allowed_moves.union(allowed_takes):
            raise IllegalMove(f"position 1: {pos_1}, position 2: {pos_2}")

        if dry_run:
            return True

        move = f"{piece.symbol}{pos_1[0]}{pos_1[1]}->"

        if pos_2 in allowed_takes:
            take_piece: Piece = self.board[pos_2[0]][pos_2[1]]
            take_piece.in_play = False
            take_piece.update_position((-1, -1))
            move = f"{move}{take_piece.symbol}{pos_2[0]}{pos_2[1]}"
        else:
            move = f"{move}{pos_2[0]}{pos_2[1]}"

        self.board[pos_1[0]][pos_1[1]] = "-"
        self.board[pos_2[0]][pos_2[1]] = piece
        piece.update_position(pos_2)

        self.moves.append(move)
        self.turn = "white" if self.turn == "black" else "black"
        self.check_completed()
        return True


if __name__ == "__main__":
    game = Game(setup="rrrr\nbrkn")
    print(game.board)
    legal_moves = game.get_all_legal_moves()
    # print(game.board[1][1].get_legal_moves(game.board))
    print(game.move((1, 0), (2, 1)))
    print(game.board)
    legal_moves = game.get_all_legal_moves()
    print(game.board)
