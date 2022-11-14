import random
from time import time

from tqdm import tqdm

from chessxtra_game import new_game, get_all_legal_moves, move_piece, colours

random.seed(1)

colours = colours()

def run_random_games(n: int = 1) -> None:
    outcomes = {colours[0]: 0, colours[1]: 0}
    for _ in tqdm(range(n)):
        game = new_game()
        # print(game.board)
        while not game.completed:
            legal_moves = get_all_legal_moves(
                game=game, colour=game.turn
            )

            chosen_piece = random.choice(list(legal_moves.keys()))
            chosen_move = random.choice(list(legal_moves[chosen_piece]))

            game = move_piece(game=game, pos_1=chosen_piece.position, pos_2=chosen_move)

            # print(game.board)
            # print()
        outcomes[game.winner] += 1
        p = 0
    print(outcomes)


def main() -> None:
    s = time()
    run_random_games(10_000)
    print(time() - s)


if __name__ == "__main__":
    main()
