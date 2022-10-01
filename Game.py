from cmath import pi
from Array import Array2D
from pieces.Piece import Piece, Position


class IllegalMove(Exception):
    pass


class Game:
    def __init__(
        self, shape: tuple[int, int] = (6, 4), setup: str = "rnbk\npppp", board_state: str or None = None
    ) -> None:
        if board_state is not None:
            shape = (len(board_state.split("\n")), len(board_state.split("\n")[0]))
        self.shape = shape
        self.board = Array2D(shape=shape)
        if board_state is None:
            self.start_setup(setup_position=setup)
        else:
            self.setup(board_state=board_state)

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

    def get_all_legal_moves(self) -> dict[Piece, set[Position]]:
        legal_moves = {}
        for row_no in range(self.board.shape[0]):
            for col_no in range(self.board.shape[1]):
                piece: Piece or str = self.board[row_no][col_no]
                if isinstance(piece, Piece):
                    legal_moves[piece] = piece.get_legal_moves(self.board)
        return legal_moves

    def check_move(self, pos_1: Position, pos_2: Position) -> bool:
        return self.move(pos_1, pos_2, dry_run=True)

    def move(self, pos_1: Position, pos_2: Position, dry_run: bool = False) -> bool:
        piece: Piece = self.board[pos_1[0]][pos_1[1]]

        allowed_moves = piece.allowed_moves(self.board)
        allowed_takes = piece.allowed_takes(self.board)

        if pos_2 not in allowed_moves.union(allowed_takes):
            raise IllegalMove(f"position 1: {pos_1}, position 2: {pos_2}")

        if dry_run:
            return True

        self.board[pos_1[0]][pos_1[1]] = "-"
        self.board[pos_2[0]][pos_2[1]] = piece
        piece.update_position(pos_2)

        if pos_2 in allowed_takes:
            take_piece: Piece = self.board[pos_2[0]][pos_2[1]]
            take_piece.in_play = False
            take_piece.update_position((-1, -1))

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
