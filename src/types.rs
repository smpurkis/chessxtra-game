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
