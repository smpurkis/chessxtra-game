mod array;
mod game;
mod pieces;
mod types;

use std::collections::HashMap;

use game::{get_all_legal_moves_with_colour, Colour};

use pieces::piece::Piece;

use types::Position;

use crate::game::Game;

use pyo3::{prelude::*};

#[pyfunction]
fn get_all_legal_moves(py_game: PyObject, colour: Colour) -> PyObject {
    Python::with_gil(|py| {
        let game: Game = py_game.extract(py).unwrap();
        let legal_moves = get_all_legal_moves_with_colour(&game, colour);
        let mut legal_moves_hashmap: HashMap<Piece, Vec<Position>> = HashMap::new();
        for (key, value) in legal_moves.into_iter() {
            legal_moves_hashmap.insert(key.clone(), value);
        }
        legal_moves_hashmap.into_py(py)
        // let legal_moves_pydict = PyDict::new(py);
        // legal_moves_pydict.
    })
}

#[pyfunction]
fn new_game() -> PyObject {
    let game = Game::new();
    Python::with_gil(|py| game.into_py(py))
}

/// A Python module implemented in Rust.
#[pymodule]
fn chessxtra_game(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(new_game, m)?)?;
    m.add_function(wrap_pyfunction!(get_all_legal_moves, m)?)?;
    Ok(())
}
