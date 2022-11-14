use std::collections::HashMap;

use pyo3::prelude::*;
use pyo3::types::PyList;
use pyo3::{pyclass, IntoPy, PyObject, PyResult, Python};

use crate::pieces::piece::{get_allowed_moves, get_allowed_takes, get_legal_moves, Piece};
use crate::types::{Array2D, PieceClass, Position, PositionContent, Shape};

#[pyclass]
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Colour {
    White,
    Black,
}

#[pyclass]
#[derive(Debug, Clone)]
pub struct Game {
    // #[pyo3(get)]
    board: Array2D,
    #[pyo3(get)]
    pub moves: Vec<String>,
    #[pyo3(get)]
    pub completed: bool,
    #[pyo3(get)]
    pub winner: Option<Colour>,
    #[pyo3(get)]
    pub turn: Colour,
    #[pyo3(get)]
    setup: String,
    #[pyo3(get)]
    shape: Shape,
}

#[pymethods]
impl Game {
    #[staticmethod]
    pub fn new() -> Self {
        let setup = "rnbk\npppp";
        let shape = Shape(6, 4);
        let game = Game {
            board: vec![vec![PositionContent::Empty; shape.1]; shape.0],
            moves: vec![],
            completed: false,
            winner: None,
            turn: Colour::White,
            setup: setup.to_owned(),
            shape,
        };

        setup_start_position(game)
    }

    #[staticmethod]
    pub fn from_position(setup: String) -> Self {
        let setup_lines = setup.split('\n').collect::<Vec<&str>>();
        assert!(
            setup_lines.iter().map(|s| s.len()).collect::<Vec<_>>()
                == vec![setup_lines[0].len(); setup_lines.len()]
        );
        let shape = Shape(setup_lines.len(), setup_lines[0].len());
        let game = Game {
            board: vec![vec![PositionContent::Empty; shape.1]; shape.0],
            moves: vec![],
            completed: false,
            winner: None,
            turn: Colour::White,
            setup: setup.to_owned(),
            shape,
        };

        setup_position(game)
    }

    #[getter]
    fn board(&self) -> PyResult<PyObject> {
        Python::with_gil(|py| {
            let pylist_array = PyList::empty(py);
            self.board.clone().into_iter().for_each(|row| {
                let pylist_row = PyList::empty(py);
                row.into_iter().for_each(|piece_content| {
                    match piece_content {
                        PositionContent::PieceContent(piece) => {
                            pylist_row.append(piece.into_py(py)).unwrap()
                        }
                        PositionContent::Empty => pylist_row.append("-").unwrap(),
                    };
                });
                pylist_array.append(pylist_row).unwrap();
            });
            Ok(pylist_array.into())
        })
    }
}

pub fn print_board(game: &Game) {
    for row in game.board.iter() {
        let mut row_str = "".to_string();
        for position_content in row.iter() {
            match position_content {
                PositionContent::PieceContent(piece) => row_str.push_str(&piece.symbol),
                PositionContent::Empty => row_str.push('-'),
            }
        }
        println!("{row_str:?}");
    }
}

fn setup_position(mut game: Game) -> Game {
    let setup_lines: Vec<Vec<char>> = game
        .setup
        .split('\n')
        .map(|s: &str| s.chars().collect())
        .collect();
    for (row_no, setup_line) in setup_lines.into_iter().enumerate() {
        for (col_no, piece_code) in setup_line.into_iter().enumerate() {
            match piece_code {
                '-' => {
                    game.board[row_no][col_no] = PositionContent::Empty;
                }
                c => {
                    let piece = Piece::new(
                        Position(row_no.try_into().unwrap(), col_no.try_into().unwrap()),
                        c.to_string(),
                    );
                    game.board[row_no][col_no] = PositionContent::PieceContent(piece)
                }
            };
        }
    }

    game
}

fn setup_start_position(mut game: Game) -> Game {
    let setup_lines: Vec<Vec<char>> = game
        .setup
        .split('\n')
        .map(|s: &str| s.chars().collect())
        .collect();
    for (piece_code, col_no) in setup_lines[0].iter().zip(0..game.shape.0) {
        let black_piece = Piece::new(
            Position(0, col_no.try_into().unwrap()),
            piece_code.to_string(),
        );
        let white_piece = Piece::new(
            Position(
                (game.shape.0 - 1).try_into().unwrap(),
                col_no.try_into().unwrap(),
            ),
            piece_code.to_string().to_uppercase(),
        );
        game.board[0][col_no] = PositionContent::PieceContent(black_piece);
        game.board[game.shape.0 - 1][col_no] = PositionContent::PieceContent(white_piece);
    }
    for (piece_code, col_no) in setup_lines[1].iter().zip(0..game.shape.0) {
        let black_piece = Piece::new(
            Position(1, col_no.try_into().unwrap()),
            piece_code.to_string(),
        );
        let white_piece = Piece::new(
            Position(
                (game.shape.0 - 2).try_into().unwrap(),
                col_no.try_into().unwrap(),
            ),
            piece_code.to_string().to_uppercase(),
        );
        game.board[1][col_no] = PositionContent::PieceContent(black_piece);
        game.board[game.shape.0 - 2][col_no] = PositionContent::PieceContent(white_piece);
    }
    game
}

fn check_completed(mut game: &mut Game) {
    let pieces = get_pieces(game);
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
        if white_king_exists && black_king_exists {
            game.winner = None;
        } else if !white_king_exists && black_king_exists {
            game.winner = Some(Colour::Black);
            game.completed = true;
        } else if white_king_exists && !black_king_exists {
            game.winner = Some(Colour::White);
            game.completed = true;
        } else {
            panic!("Should not get here")
        }
    }
}

pub fn get_all_legal_moves_with_colour(
    game: &Game,
    colour: Colour,
) -> HashMap<&Piece, Vec<Position>> {
    let mut legal_moves = HashMap::new();
    // get_pieces(&game).into_iter().for_each(|p| println!("{:?}", p));
    let colour_pieces = get_pieces_with_colour(game, colour);
    colour_pieces.into_iter().for_each(|piece| {
        if piece.in_play {
            let piece_legal_moves: Vec<Position> = get_legal_moves(piece, &game.board, &game.shape);
            if !piece_legal_moves.is_empty() {
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
                PositionContent::PieceContent(piece) => {
                    if piece.colour == colour {
                        pieces.push(piece);
                    }
                }
                PositionContent::Empty => (),
            };
        }
    }
    pieces
}

fn check_move(game: &mut Game, pos_1: Position, pos_2: Position) -> bool {
    move_piece(game, pos_1, pos_2, true)
}

pub fn move_piece(game: &mut Game, pos_1: Position, pos_2: Position, dry_run: bool) -> bool {
    let piece: &PositionContent =
        &game.board[usize::try_from(pos_1.0).unwrap()][usize::try_from(pos_1.1).unwrap()];

    match piece {
        PositionContent::Empty => panic!("Tried to move an empty square!"),
        PositionContent::PieceContent(piece) => {
            let allowed_moves = get_allowed_moves(piece, &game.board, &game.shape);
            let allowed_takes = get_allowed_takes(piece, &game.board, &game.shape);

            let mut allowed_new_positions: Vec<&Position> =
                Vec::with_capacity(allowed_moves.len() + allowed_takes.len());
            allowed_new_positions.extend(&allowed_moves);
            allowed_new_positions.extend(&allowed_takes);
            allowed_new_positions.sort_unstable();
            allowed_new_positions.dedup();

            if !allowed_new_positions.contains(&&pos_2) {
                panic!["Illegal move detected!"]
            }

            if dry_run {
                return true;
            }

            let mut move_str = format!("{0}{1}{2}->", piece.symbol, pos_1.0, pos_1.1);

            let take_piece: &mut PositionContent = &mut game.board
                [usize::try_from(pos_2.0).unwrap()][usize::try_from(pos_2.1).unwrap()];
            match take_piece {
                PositionContent::PieceContent(take_piece) => {
                    take_piece.in_play = false;
                    take_piece.position = Position(-1, -1);
                    move_str = format!(
                        "{0}{1:?}{2}{3}",
                        move_str, take_piece.position, pos_2.0, pos_2.1
                    );
                }
                PositionContent::Empty => {
                    move_str = format!("{0}{1}{2}", move_str, pos_2.0, pos_2.1);
                }
            }

            let piece: &mut PositionContent = &mut game.board[usize::try_from(pos_1.0).unwrap()]
                [usize::try_from(pos_1.1).unwrap()];

            match piece {
                PositionContent::PieceContent(piece) => {
                    piece.position = pos_2.clone();
                }
                PositionContent::Empty => panic!("Tried to move an empty square!"),
            }
            game.moves.push(move_str);

            game.board[usize::try_from(pos_2.0).unwrap()][usize::try_from(pos_2.1).unwrap()] =
                piece.clone();
            game.board[usize::try_from(pos_1.0).unwrap()][usize::try_from(pos_1.1).unwrap()] =
                PositionContent::Empty;

            game.turn = if game.turn == Colour::Black {
                Colour::White
            } else {
                Colour::Black
            };
            check_completed(game);
        }
    }

    true
}
