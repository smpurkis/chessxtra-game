use std::fmt::Display;

use pyo3::{pyclass, IntoPy, PyObject};

use crate::pieces::piece::Piece;

#[derive(Clone, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct Position(pub isize, pub isize);

impl IntoPy<PyObject> for Position {
    fn into_py(self, py: pyo3::Python<'_>) -> PyObject {
        (self.0, self.1).into_py(py)
    }
}

#[derive(Clone, Debug)]
pub struct Shape(pub usize, pub usize);

impl IntoPy<PyObject> for Shape {
    fn into_py(self, py: pyo3::Python<'_>) -> PyObject {
        (self.0, self.1).into_py(py)
    }
}

#[derive(Debug, Clone)]
pub enum PositionContent {
    PieceContent(Piece),
    Empty,
}

impl Display for PositionContent {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            PositionContent::PieceContent(piece) => write!(f, "{}", piece.symbol),
            PositionContent::Empty => write!(f, "-"),
        }
    }
}

#[pyclass]
#[derive(Clone, Copy, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub(crate) enum PieceClass {
    King,
    Queen,
    Rook,
    Bishop,
    Knight,
    Pawn,
}

pub type Array2D = Vec<Vec<PositionContent>>;
