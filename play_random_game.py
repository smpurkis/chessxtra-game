import random
from time import time

from Game import Game
from tqdm import tqdm

random.seed(1)


def run_random_games(n: int = 1) -> None:
    outcomes = {"white": 0, "black": 0}
    for _ in tqdm(range(n)):
        game = Game()
        # print(game.board)
        while not game.completed:
            legal_moves = None
            if game.turn == "white":
                legal_moves = game.get_all_legal_moves(
                    colour="white", include_empty=False
                )
            elif game.turn == "black":
                legal_moves = game.get_all_legal_moves(
                    colour="black", include_empty=False
                )

            chosen_piece = random.choice(list(legal_moves.keys()))
            chosen_move = random.choice(list(legal_moves[chosen_piece]))

            game.move(chosen_piece.position, chosen_move)

            # print(game.board)
            # print()
        outcomes[game.winner] += 1
        p = 0
    print(outcomes)


def main() -> None:
    s = time()
    run_random_games(1000)
    print(time() - s)


if __name__ == "__main__":
    main()
