mod array;
mod game;
mod pieces;
mod types;

use std::collections::HashMap;

use game::{get_all_legal_moves_with_colour, Colour, move_piece_position};

use pieces::piece::Piece;

use types::Position;

use crate::game::Game;

use pyo3::{prelude::*, types::PyTuple};



#[pyfunction]
fn new_game() -> PyObject {
    let game = Game::new();
    Python::with_gil(|py| game.into_py(py))
}

#[pyfunction]
fn get_all_legal_moves(game: PyObject, colour: Colour) -> PyObject {
    Python::with_gil(|py| {
        let game: Game = game.extract(py).unwrap();
        let legal_moves = get_all_legal_moves_with_colour(&game, colour);
        let mut legal_moves_hashmap: HashMap<Piece, Vec<Position>> = HashMap::new();
        for (key, value) in legal_moves.into_iter() {
            legal_moves_hashmap.insert(key.clone(), value);
        }
        legal_moves_hashmap.into_py(py)
    })
}

#[pyfunction]
fn move_piece(game: PyObject, pos_1: PyObject, pos_2: PyObject) -> PyObject {
    Python::with_gil(|py| {
        let mut game: Game = game.extract(py).unwrap();
        let pos_1: (isize, isize) = pos_1.extract(py).unwrap();
        let pos_1 = Position(pos_1.0, pos_1.1);
        let pos_2: (isize, isize) = pos_2.extract(py).unwrap();
        let pos_2 = Position(pos_2.0, pos_2.1);
        move_piece_position(&mut game, pos_1, pos_2, false);
        game.into_py(py)
    })
}

#[pyfunction]
fn colours() -> PyObject {
    Python::with_gil(|py| {
        vec![Colour::White, Colour::Black].into_py(py)
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn chessxtra_game(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(new_game, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_legal_moves, m)?)?;
    m.add_function(wrap_pyfunction!(move_piece, m)?)?;
    m.add_function(wrap_pyfunction!(colours, m)?)?;
    Ok(())
}
