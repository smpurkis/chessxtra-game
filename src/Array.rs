use std::ops::Index;

use crate::types::{Position, Shape};

pub(crate) fn check_position_is_on_board(pos: &Position, shape: &Shape) -> bool {
    (0 <= pos.0 && pos.0 + 1 <= shape.0.try_into().unwrap()) && (0 <= pos.1 && pos.1 + 1 <= shape.1.try_into().unwrap())
}

fn dist(pos1: &Position, pos2: &Position) -> isize {
    (pos1.0 - pos2.0) - (pos1.1 - pos2.1)
}

fn filter_positions_off_board(positions: Vec<Position>, shape: &Shape) -> Vec<Position> {
    positions
        .into_iter()
        .filter(|pos| check_position_is_on_board(&pos, shape))
        .collect()
}

pub(crate) fn get_col_row_positions(
    pos: &Position, shape: &Shape
) -> (Vec<Vec<Position>>, Vec<Vec<Position>>) {
    let mut new_positions = Vec::with_capacity(shape.0);
    for i in 0..shape.0 {
        new_positions.push(Position(i.try_into().unwrap(), pos.1))
    }

    let column_positions = split_at_position(filter_positions_off_board(new_positions, shape), pos);

    let mut new_positions = Vec::with_capacity(shape.0);
    for i in 0..shape.1 {
        new_positions.push(Position(pos.0, i.try_into().unwrap()))
    }

    let row_positions = split_at_position(filter_positions_off_board(new_positions, shape), pos);
    (column_positions, row_positions)
}

pub(crate) fn get_l_positions(pos: &Position, board_shape: &Shape) -> Vec<Position> {
    let l_offsets = vec![(-1, 2), (1, 2), (-1, -2), (1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)];
    let mut new_positions: Vec<Position> = Vec::with_capacity(l_offsets.len());
    for (i, j) in l_offsets {
        new_positions.push(Position(pos.0 + i, pos.1 + j))
    }
    let positions = filter_positions_off_board(
        new_positions, board_shape
    );
    positions
}


pub(crate) fn get_surrounding_positions(positions: Vec<Position>, pos: Position, shape: &Shape) -> Vec<Position> {
    let mut new_positions: Vec<Position> = Vec::with_capacity(3*positions.len());
    for i in -1_isize..=1 {
        for j in -1_isize..=1 {
            new_positions.push(Position(pos.0 + i, pos.1 + j))
        }
    }
    let filtered_positions = filter_positions_off_board(new_positions, shape);
    filtered_positions
}

fn split_at_position(positions: Vec<Position>, pos: &Position) -> Vec<Vec<Position>> {
    let index = 1;
    // TODO: May be able to remove .to_vec() and speed up by reducing allocations
    vec![positions[0..index].to_vec(), positions[(index+1)..positions.len()].to_vec()]
}

fn sort_by_distance(pos: Position, positions: Vec<Position>) -> Vec<Position> {
    let mut position_distances: Vec<(isize, Position)>= positions
    .into_iter()
    .map(|p| (dist(&pos, &p), p))
    .collect();
    position_distances.sort_by(|a, b| a.0.cmp(&b.0));
    let positions: Vec<Position> = position_distances.into_iter().map(|(d, p)| p).collect();
    positions
}