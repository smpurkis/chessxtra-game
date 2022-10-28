use crate::types::{Array2D, Position};

use super::piece::Piece;

pub(crate) fn allowed_moves(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    is_white: bool,
) -> Vec<Position> {
    vec![]
}

pub(crate) fn allowed_takes(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    is_white: bool,
) -> Vec<Position> {
    vec![]
}
