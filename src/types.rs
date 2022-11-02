use std::fmt::{format, write, Display};

use crate::pieces::piece::Piece;

#[derive(Clone, Debug, Hash, PartialEq, Eq, PartialOrd, Ord)]
pub struct Position(pub isize, pub isize);

#[derive(Clone, Debug)]
pub struct Shape(pub usize, pub usize);

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
