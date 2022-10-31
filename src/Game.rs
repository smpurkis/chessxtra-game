use std::collections::HashMap;

use crate::pieces::piece::{get_legal_moves, Piece, get_allowed_moves, get_allowed_takes};
use crate::types::{Array2D, PieceClass, Position, PositionContent, Shape};

enum Colour {
    White,
    Black,
}

struct Game {
    board: Array2D,
    moves: Vec<String>,
    completed: bool,
    winner: Option<Colour>,
    turn: Colour,
    setup: String,
    shape: Shape,
}

impl Game {
    pub fn new() -> Self {
        let setup = "rnbk\npppp";
        let shape = Shape(6, 4);
        let game = Game {
            board: vec![vec![PositionContent::Empty; shape.0]; shape.1],
            moves: vec![],
            completed: false,
            winner: None,
            turn: Colour::White,
            setup: setup.to_owned(),
            shape: shape,
        };
        let game = setup_position(game);
        game
    }
}

fn setup_position(mut game: Game) -> Game {
    let setup_lines: Vec<Vec<char>> = game
        .setup
        .split("\n")
        .map(|s: &str| s.chars().collect())
        .collect();
    for (piece_code, col_no) in setup_lines[0].iter().zip(0..game.shape.0) {
        let piece = Piece::new(
            Position(0, col_no.try_into().unwrap()),
            piece_code.to_string(),
        );
        game.board[0][col_no] = PositionContent::PieceContent(piece);
    }

    game
}

fn check_completed(mut game: Game) {
    let pieces = get_pieces(&game);
    let white_pieces: Vec<&&Piece> = pieces.iter().filter(|p: &&&Piece| p.is_white).collect();
    let black_pieces: Vec<&&Piece> = pieces.iter().filter(|p: &&&Piece| !p.is_white).collect();
    let white_king_exists = white_pieces
        .iter()
        .filter(|p: &&&&Piece| p.full_symbol == PieceClass::King)
        .count()
        == 1;
    let black_king_exists = black_pieces
        .iter()
        .filter(|p: &&&&Piece| p.full_symbol == PieceClass::King)
        .count()
        == 1;

    if !game.completed {
        if white_king_exists || black_king_exists {
            game.winner = None;
        } else if !white_king_exists || black_king_exists {
            game.winner = Some(Colour::Black);
            game.completed = true;
        } else if white_king_exists || !black_king_exists {
            game.winner = Some(Colour::White);
            game.completed = true;
        } else {
            panic!("Should not get here")
        }
    }
}

fn get_all_legal_moves_with_colour(game: &Game, colour: Colour) -> HashMap<&Piece, Vec<Position>> {
    let mut legal_moves = HashMap::new();
    let white_pieces = get_pieces_with_colour(&game, Colour::White);
    white_pieces.into_iter().for_each(|piece| {
        if piece.in_play {
            let piece_legal_moves: Vec<Position> = get_legal_moves(piece, &game.board, &game.shape);
            if piece_legal_moves.len() > 0 {
                legal_moves.insert(piece, piece_legal_moves);
            }
        }
    });
    legal_moves
}

fn get_pieces(game: &Game) -> Vec<&Piece> {
    let mut pieces = Vec::with_capacity(16);
    for row in &game.board {
        for square in row {
            match square {
                PositionContent::PieceContent(piece) => pieces.push(piece),
                PositionContent::Empty => (),
            };
        }
    }
    pieces
}

fn get_pieces_with_colour<'a>(game: &'a Game, colour: Colour) -> Vec<&'a Piece> {
    let mut pieces = Vec::with_capacity(16);
    for row in &game.board {
        for square in row {
            match square {
                PositionContent::PieceContent(piece) => pieces.push(piece),
                PositionContent::Empty => (),
            };
        }
    }
    pieces
}

fn check_move(game: &mut Game, pos_1: &Position, pos_2: &Position) -> bool {
    move_pos(game, pos_1, pos_2, true)
}


fn move_pos(game: &mut Game, pos_1: &Position, pos_2: &Position, dry_run: bool) -> bool {
    let piece: &PositionContent = &game.board[usize::try_from(pos_1.0).unwrap()][usize::try_from(pos_1.1).unwrap()];    
    
    match piece {
        PositionContent::Empty => panic!("Tried to move an empty square!"),
        PositionContent::PieceContent(piece) => {
            let allowed_moves = get_allowed_moves(piece, &game.board, &game.shape);
            let allowed_takes = get_allowed_takes(piece, &game.board, &game.shape);
        
            let mut allowed_new_positions: Vec<&Position> = Vec::with_capacity(allowed_moves.len() + allowed_takes.len());
            allowed_new_positions.extend(&allowed_moves);
            allowed_new_positions.extend(&allowed_takes);
            allowed_new_positions.sort_unstable();
            allowed_new_positions.dedup();

            if allowed_new_positions.contains(&pos_2) {
                panic!["Illegal move detected!"]
            }

            if dry_run {
                return true;
            }

            // let move_str = format!("{0}{1}{2}->", piece.symbol, pos_1.0, pos_1.1);

            if allowed_takes.contains(pos_2) {
                let take_piece: &mut PositionContent = &mut game.board[usize::try_from(pos_2.0).unwrap()][usize::try_from(pos_2.1).unwrap()];    
                match take_piece {
                    PositionContent::PieceContent(take_piece) => {
                        take_piece.in_play = false;
                        take_piece.position = Position(-1, -1);
                    },
                    PositionContent::Empty => (),
                }
            }
        },
    }
    
    true
}