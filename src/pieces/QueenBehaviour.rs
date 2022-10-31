use crate::{types::{Array2D, Position, Shape, PositionContent}, Array::{sort_by_distance, get_diagonal_positions, get_col_row_positions}};

use super::piece::Piece;

pub(crate) fn allowed_moves(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    let col_row_positions = get_col_row_positions(pos, shape);
    let diagonal_positions = get_diagonal_positions(pos, shape);
    let mut position_lines = Vec::with_capacity(2 + diagonal_positions.len());
    for positions in col_row_positions.into_iter() {
        position_lines.push(positions)
    }
    for positions in diagonal_positions.into_iter() {
        position_lines.push(positions)
    }
    let mut filt_all_ms: Vec<Position> = Vec::with_capacity(20);
    for positions in position_lines.into_iter() {
        for dir_positions in positions {
            let dir_positions = sort_by_distance(pos, dir_positions);
            for move_pos in dir_positions.into_iter() {
                let mp_piece: &PositionContent = &board[usize::try_from(move_pos.0).unwrap()]
                    [usize::try_from(move_pos.1).unwrap()];
                match mp_piece {
                    PositionContent::PieceContent(_) => filt_all_ms.push(move_pos),
                    PositionContent::Empty => break,
                }
            }
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
    let col_row_positions = get_col_row_positions(pos, shape);
    let diagonal_positions = get_diagonal_positions(pos, shape);
    let mut position_lines = Vec::with_capacity(2 + diagonal_positions.len());
    for positions in col_row_positions.into_iter() {
        position_lines.push(positions)
    }
    for positions in diagonal_positions.into_iter() {
        position_lines.push(positions)
    }
    let mut filt_all_ts: Vec<Position> = Vec::with_capacity(20);
    for positions in position_lines.into_iter() {
        for dir_positions in positions {
            let dir_positions = sort_by_distance(pos, dir_positions);
            for take_pos in dir_positions.into_iter() {
                let tp_piece: &PositionContent = &board[usize::try_from(take_pos.0).unwrap()]
                    [usize::try_from(take_pos.1).unwrap()];
                match tp_piece {
                    PositionContent::PieceContent(tp_piece) => {
                        if tp_piece.is_white != piece.is_white {
                            filt_all_ts.push(take_pos)
                        }
                        break
                    },
                    PositionContent::Empty => break,
                }
            }
        }
    }
    filt_all_ts
}
