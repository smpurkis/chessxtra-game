import random
from time import time

from tqdm import tqdm

from Game import initialize_game, get_all_legal_moves, move

random.seed(1)


#
def run_random_games(n: int = 1) -> None:
    outcomes = {"white": 0, "black": 0}
    for _ in tqdm(range(n)):
        game = initialize_game()
        # print(game.board)
        while not game.completed:
            if game.turn == "white":
                legal_moves = get_all_legal_moves(
                    game=game, colour="white", include_empty=False
                )
            elif game.turn == "black":
                legal_moves = get_all_legal_moves(
                    game=game, colour="black", include_empty=False
                )

            chosen_piece = random.choice(list(legal_moves.keys()))
            chosen_move = random.choice(list(legal_moves[chosen_piece]))

            move(game=game, pos_1=chosen_piece.position, pos_2=chosen_move)

            # print(game.board)
            # print()
        outcomes[game.winner] += 1
        p = 0
    print(outcomes)


def main() -> None:
    s = time()
    run_random_games(500)
    print(time() - s)


if __name__ == "__main__":
    main()
