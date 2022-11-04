use crate::{
    array::check_position_is_on_board,
    types::{Array2D, Position, PositionContent, Shape},
};

use super::piece::Piece;

pub(crate) fn allowed_moves(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    let index: isize = if is_white { -1 } else { 1 };
    let new_positions = vec![Position(pos.0 + index, pos.1)];
    let new_positions: Vec<Position> = new_positions
        .into_iter()
        .filter(|p| check_position_is_on_board(p, shape))
        .collect();
    let mut filt_all_ms: Vec<Position> = Vec::with_capacity(new_positions.len());
    for move_pos in new_positions.into_iter() {
        let mp_piece: &PositionContent =
            &board[usize::try_from(move_pos.0).unwrap()][usize::try_from(move_pos.1).unwrap()];
        match mp_piece {
            PositionContent::PieceContent(_) => (),
            PositionContent::Empty => filt_all_ms.push(move_pos),
        }
    }
    filt_all_ms
}

pub(crate) fn allowed_takes(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    let index: isize = if is_white { -1 } else { 1 };
    let new_positions = vec![Position(pos.0 + index, pos.1)];
    let new_positions: Vec<Position> = new_positions
        .into_iter()
        .filter(|p| check_position_is_on_board(p, shape))
        .collect();
    let mut filt_all_ts: Vec<Position> = Vec::with_capacity(new_positions.len());
    for take_pos in new_positions.into_iter() {
        let tp_piece: &PositionContent =
            &board[usize::try_from(take_pos.0).unwrap()][usize::try_from(take_pos.1).unwrap()];
        match tp_piece {
            PositionContent::PieceContent(_) => filt_all_ts.push(take_pos),
            PositionContent::Empty => (),
        }
    }
    filt_all_ts
}
