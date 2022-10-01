from Game import Game
import json
from pathlib import Path
from Array import Position
from pieces.Piece import Piece, ALLOWED_PIECE_CODES
import random


def convert_moves_to_json(
    legal_moves: dict[Piece, set[Position]]
) -> dict[str, tuple[Position]]:
    json_legal_moves = {}
    for p, ms in legal_moves.items():
        json_legal_moves[p.__repr__()] = tuple(ms)
    return json_legal_moves


def random_board_state() -> set[str]:
    piece_codes = ("k", "q", "r", "b", "n", "p", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-")
    setup_strings = []
    for _ in range(10):
        setup = []
        n = 6
        for i in range(n):
            setup_row = [random.choice(piece_codes) for _ in range(4)]
            setup.extend(setup_row)
            if i < n - 1:
                setup.append("\n")
        setup_str = "".join(setup)
        setup_strings.append(setup_str)
    return set(setup_strings)


def test_check_legal_moves():
    board_states_legal_moves = {
        "----\n-p--\nP-P-\n----\n----\n----": None,
        "----\nk---\n-p--\n----\n----\n----": None,
        "----\n-n--\n----\n--P-\n----\n----": None,
        "----\n-b--\n----\n---P\n----\n----": None,
        "----\n-r--\n----\n----\n----\n-P--": None,
        "----\n-q--\n--P-\n---P\n----\n-P--": None,
        "rnbk\npppp\n----\n----\nPPPP\nRNBK": None,
        "----\n----\n----\n----\n----\n----": None,
    }
    save_path = Path("tests", "data", "board_states_legal_moves.json")
    board_states_legal_moves = json.load(save_path.open())
    for setup_str in board_states_legal_moves:
        setup_str_dash = setup_str.replace('\n', '-')

        game = Game(board_state=setup_str)
        legal_moves = game.get_all_legal_moves()
        board_states_legal_moves[setup_str] = convert_moves_to_json(legal_moves)
        # ground_truth_legal_moves = convert_moves_to_json(legal_moves)
        # assert convert_moves_to_json(legal_moves) == ground_truth_legal_moves
    save_path.parent.mkdir(parents=True, exist_ok=True)
    json.dump(
        board_states_legal_moves,
        save_path.open("w"),
        sort_keys=True,
        indent=4,
    )

# print(random_board_state())
test_check_legal_moves()