use crate::types::{Array2D, Position, PositionContent, Shape};

use super::piece::Piece;

pub(crate) fn allowed_moves(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    // let surrounding_positions = get_d(pos, shape);
    // let mut filt_all_ms: Vec<Position> = Vec::with_capacity(surrounding_positions.len());
    // for move_pos in surrounding_positions.into_iter(){
    //     ̣et mp_piece: &PositionContent = &board[usize::try_from(move_pos.0).unwrap()][usize::try_from(move_pos.1).unwrap()];
    //     match mp_piece {
    //         PositionContent::PieceContent(_) => (),
    //         PositionContent::Empty => filt_all_ms.push(move_pos),
    //     }
    // }
    // filt_all_ms
    vec![]
}

pub(crate) fn allowed_takes(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    vec![]
}
