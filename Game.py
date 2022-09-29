from cmath import pi
from Array import Array2D
from pieces.Piece import Piece, Position


class Game:
    def __init__(
        self, shape: tuple[int, int] = (6, 4), setup: str = "rnbk\npppp"
    ) -> None:
        self.shape = shape
        self.board = Array2D(shape=shape)
        self.setup(setup_position=setup)

    def setup(self, setup_position: str):
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

    def get_allowed_moves(self, pos: Position) -> set[Position]:
        piece: Piece = self.board[pos[1]][pos[0]]
        allowed_moves = piece.allowed_moves()
        filt_all_ms = set()
        for move_pos in allowed_moves:
            mp_piece = self.board[move_pos[1], move_pos[0]]
            if isinstance(mp_piece, Piece):
                if mp_piece.is_white == piece.is_white:
                    filt_all_ms.add(move_pos)

        allowed_takes = piece.allowed_takes()
        filt_all_ts = set()
        for take_pos in allowed_takes:
            tp_piece = self.board[take_pos[1], take_pos[0]]
            if isinstance(tp_piece, Piece):
                if tp_piece.is_white == piece.is_white:
                    filt_all_ts.add(take_pos)

    # def check_move(self, pos_1: Position, pos_2: Position) -> bool:
    #     return self.move(pos_1, pos_2, dry_run=True)

    # def move(self, pos_1: Position, pos_2: Position, dry_run: bool = False) -> bool:
    #     piece: Piece = self.board[pos_1[1]][pos_1[0]]

    #     allowed_moves = piece.allowed_moves()

    #     take_piece: Piece or None = (
    #         self.board[pos_2[1]][pos_2[0]]
    #         if isinstance(self.board[pos_2[1]][pos_2[0]], Piece)
    #         else None
    #     )
    #     if take_piece is not None:
    #         allowed_takes = piece.allowed_takes(take_piece)
    #     else:
    #         allowed_takes = set()

    #     print(pos_2, allowed_moves.union(allowed_takes))
    #     if pos_2 not in allowed_moves.union(allowed_takes):
    #         return False
    #     if not dry_run:
    #         self.board[pos_1[1]][pos_1[0]] = "-"
    #         self.board[pos_2[1]][pos_2[0]] = piece
    #         piece.update_position(pos_2)
    #         if take_piece is not None:
    #             take_piece.in_play = False
    #             take_piece.position = (-1, -1)
    #     return True


if __name__ == "__main__":
    game = Game(setup="rrrr\npppp")
    print(game.board)
    legal_moves = game.get_all_legal_moves()
    # print(game.board[1][1].get_legal_moves(game.board))
    # print(game.move((0, 1), (0, 2)))
    print(game.board)
