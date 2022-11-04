mod array;
mod game;
mod pieces;
mod types;
use std::time::Instant;

use game::{get_all_legal_moves_with_colour, move_piece, Colour};
use rand::{prelude::StdRng, seq::SliceRandom, SeedableRng};

use crate::game::{print_board, Game};

#[derive(Debug)]
struct Outcomes {
    white: usize,
    black: usize,
}

fn run_random_games(n: usize) {
    let mut outcomes = Outcomes { white: 0, black: 0 };
    // let mut rng = rand::thread_rng();
    let mut rng = StdRng::seed_from_u64(0);
    for _ in 0..n {
        let mut game = Game::new();
        // let setup = "--PK\n--kp\n-p-P\npP--\nP---\n----";
        // let mut game = Game::from_position(setup.to_string());
        while !game.completed {
            let legal_moves = get_all_legal_moves_with_colour(&game, game.turn.clone());
            if legal_moves.len() == 0 {
                print_board(&game);
                println!("no moves");
            }
            if game.moves.len() > 10_000 {
                print_board(&game);
                println!("Too many moves");
            }
            let chosen_piece = &**legal_moves
                .keys()
                .into_iter()
                .collect::<Vec<_>>()
                .choose(&mut rng)
                .unwrap()
                .clone();
            let chosen_move = legal_moves
                .get(&chosen_piece)
                .unwrap()
                .choose(&mut rng)
                .unwrap()
                .clone();
            let chosen_piece_pos = chosen_piece.position.clone();

            move_piece(&mut game, chosen_piece_pos, chosen_move, false);
        }

        match game.winner {
            Some(winner) => match winner {
                Colour::White => outcomes.white += 1,
                Colour::Black => outcomes.black += 1,
            },
            None => panic!("There must be a winner!"),
        }
    }
    println!("{:?}", outcomes);
}

fn main() {
    let timer = Instant::now();
    run_random_games(10_000);
    println!("{:?}", timer.elapsed());
}
