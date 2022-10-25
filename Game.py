from dataclasses import dataclass
from typing import Dict, Optional, Tuple, Union, List

from Array import Array2D

# import numpy as np
from pieces.Piece import (
    Piece,
    Position,
    get_allowed_moves,
    get_allowed_takes,
    get_legal_moves,
    make_piece,
)


class IllegalMove(Exception):
    pass


@dataclass
class Game:
    board: Array2D
    moves: List[str]
    completed: bool
    winner: str
    turn: str
    setup: str
    shape: Tuple[int, int]
    board_state: Optional[str]


# @profile
def initialize_game(
    shape: Tuple[int, int] = (6, 4),
    setup: str = "rnbk\npppp",
    board_state: Optional[str] = None,
) -> Game:
    if board_state is not None:
        shape = (len(board_state.split("\n")), len(board_state.split("\n")[0]))
    game = Game(
        shape=shape,
        setup=setup,
        board=Array2D(shape=shape),
        # board=np.full(shape=shape, fill_value="-", dtype=object),
        board_state=board_state,
        completed=False,
        moves=[],
        turn="white",
        winner="",
    )
    if board_state is None:
        game = start_setup(game=game, setup_position=setup)
    else:
        game = setup_position(game=game, board_state=board_state)
    return game


# @profile
def check_completed(game: Game) -> None:
    pieces = get_pieces(game=game)
    white_pieces = {p for p in pieces if p.is_white}
    black_pieces = {p for p in pieces if not p.is_white}
    white_king_exists = len({p for p in white_pieces if p.full_symbol == "KING"}) == 1
    black_king_exists = len({p for p in black_pieces if p.full_symbol == "KING"}) == 1
    if not game.completed:
        if white_king_exists and black_king_exists:
            game.winner = "neither"
        elif not white_king_exists and black_king_exists:
            game.winner = "black"
            game.completed = True
        elif white_king_exists and not black_king_exists:
            game.winner = "white"
            game.completed = True
    else:
        raise Exception("should not get here")


# @profile
def setup_position(game: Game, board_state: str) -> Game:
    setup_lines = board_state.split("\n")
    for row_no, lines in enumerate(setup_lines):
        for col_no, piece_code in enumerate(lines):
            if piece_code == "-":
                game.board[row_no][col_no] = "-"
            else:
                game.board[row_no][col_no] = make_piece((row_no, col_no), piece_code)
    return game


# @profile
def start_setup(game: Game, setup_position: str) -> Game:
    setup_lines = setup_position.split("\n")
    for piece_code, col_no in zip(setup_lines[0], range(game.board.shape[1])):
        game.board[0][col_no] = make_piece((0, col_no), piece_code)
        game.board[-1][col_no] = make_piece(
            (game.board.shape[0] - 1, col_no), piece_code.upper()
        )

    if len(setup_lines) > 1:
        for piece_code, col_no in zip(setup_lines[1], range(game.board.shape[1])):
            game.board[1][col_no] = make_piece((1, col_no), piece_code)
            game.board[-2][col_no] = make_piece(
                (game.board.shape[0] - 2, col_no), piece_code.upper()
            )
    return game


# @profile
def get_all_legal_moves(
    game: Game, colour: Optional[str] = None, include_empty: bool = True
) -> Dict[Piece, List[Position]]:
    legal_moves = {}
    for row_no in range(game.board.shape[0]):
        for col_no in range(game.board.shape[1]):
            piece: Union[Piece, str] = game.board[row_no][col_no]
            if isinstance(piece, Piece):
                if colour is None or piece.colour == colour and piece.in_play:
                    piece_legal_moves = get_legal_moves(piece, game.board)
                    if len(piece_legal_moves) > 0 or include_empty:
                        legal_moves[piece] = piece_legal_moves
    return legal_moves


# @profile
def get_pieces(game: Game, colour: Optional[str] = None) -> List[Piece]:
    pieces = []
    for row_no in range(game.board.shape[0]):
        for col_no in range(game.board.shape[1]):
            piece: Union[Piece, str] = game.board[row_no][col_no]
            if isinstance(piece, Piece):
                if colour is None or piece.colour == colour and piece.in_play:
                    pieces.append(piece)
    return pieces


# @profile
def check_move(game: Game, pos_1: Position, pos_2: Position) -> bool:
    return move(game=game, pos_1=pos_1, pos_2=pos_2, dry_run=True)


# @profile
def move(game: Game, pos_1: Position, pos_2: Position, dry_run: bool = False) -> bool:
    piece: Piece = game.board[pos_1[0]][pos_1[1]]

    allowed_moves = get_allowed_moves(piece, game.board)
    allowed_takes = get_allowed_takes(piece, game.board)

    if pos_2 not in set(allowed_moves + allowed_takes):
        raise IllegalMove(f"position 1: {pos_1}, position 2: {pos_2}")

    if dry_run:
        return True

    move = f"{piece.symbol}{pos_1[0]}{pos_1[1]}->"

    if pos_2 in allowed_takes:
        take_piece: Piece = game.board[pos_2[0]][pos_2[1]]
        take_piece.in_play = False
        take_piece.position = (-1, -1)
        move = f"{move}{take_piece.symbol}{pos_2[0]}{pos_2[1]}"
    else:
        move = f"{move}{pos_2[0]}{pos_2[1]}"

    game.board[pos_1[0]][pos_1[1]] = "-"
    game.board[pos_2[0]][pos_2[1]] = piece
    piece.position = pos_2

    game.moves.append(move)
    game.turn = "white" if game.turn == "black" else "black"
    check_completed(game=game)
    return True
