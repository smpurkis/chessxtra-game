mod array;
mod game;
mod pieces;
mod types;
use game::{get_all_legal_moves_with_colour, Colour};
use rand::thread_rng;
use rand::seq::SliceRandom;

use crate::game::Game;

struct Outcomes {
    white: usize,
    black: usize,
}

fn run_random_games(n: usize) {
    let outcomes = Outcomes { white: 0, black: 0 };
    let mut rng = rand::thread_rng();
    for _ in 0..n {
        let game = Game::new();
        while !game.completed {
            let legal_moves = get_all_legal_moves_with_colour(&game, game.turn.clone());
            let chosen_piece = legal_moves.keys();
            let chosen_move = ;
        }
    }
}

fn main() {}
