import { Position, Shape } from "./custom_types";
import { range } from "./Game";
import { Piece } from "./pieces/Piece";

export interface Array2D {
    shape: Shape;
    data: Piece[][]
}

function dist(pos1: Position, pos2: Position): number {
    return Math.abs(pos1[0] - pos2[0]) - Math.abs(pos1[1] - pos2[1])
}

export function check_position_is_on_board(position: Position, board_shape: Shape): boolean {
    return (0 <= position[0] && position[0] <= board_shape[0] - 1) && (0 <= position[1] && position[1] <= board_shape[1] - 1)
}

export function filter_positions_off_board_list(positions: Position[], board_shape: Shape): Position[] {
    const filtered_positions: Position[] = []
    positions.forEach((pos: Position) => {
        if (check_position_is_on_board(pos, board_shape)) {
            filtered_positions.push(pos)
        }
    })
    return filtered_positions
}

export function sort_by_distance(pos: Position, positions: Position[]): Position[] {
    const position_distances: [number, Position][] = []
    positions.forEach((p) => {
        position_distances.push([dist(pos, p), p])
    })
    position_distances.sort((a: [number, Position], b: [number, Position]) => a[0] - b[0])
    const distances: Position[] = position_distances.map((v) => v[1])
    return distances
}

function split_at_position(positions: Position[], pos: Position): Position[][] {
    const index = positions.indexOf(pos)
    const positions_1 = positions.slice(0, index)
    const positions_2 = positions.slice(index + 1, positions.length)
    return [positions_1, positions_2]
}

export function get_surrounding_positions(pos: Position, board_shape: Shape): Position[] {
    const indices: number[] = [-1, 0, 1]
    let positions: Position[] = []
    indices.forEach((i: number) => {
        indices.forEach((j: number) => {
            positions.push([pos[0] + i, pos[1] + j])
        })
    })
    positions = filter_positions_off_board_list(positions, board_shape)
    return positions
}

const l_offsets: Position[] = [[-1, 2], [1, 2], [-1, -2], [1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1]]
export function get_l_positions(pos: Position, board_shape: Shape): Position[] {
    let positions: Position[] = l_offsets.map((ij: number[]) => [pos[0] + ij[0], pos[1] + ij[1]])
    positions = filter_positions_off_board_list(positions, pos)
    return positions
}


export function get_col_row_positions(pos: Position, board_shape: Shape): Position[][][] {
    const col_range = board_shape[0]
    const row_range = board_shape[1]

    const col_positions: Position[] = range(col_range).map((i) => [i, pos[1]])
    const column_positions = split_at_position(
        filter_positions_off_board_list(
            col_positions, board_shape
        ), 
        pos
    )
    const r_positions: Position[] = range(col_range).map((i) => [pos[0], i])
    const row_positions = split_at_position(
        filter_positions_off_board_list(
            r_positions, board_shape
        ), 
        pos
    )
    return [column_positions, row_positions]
}


const diagonal_range: Position[] = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
export function get_diagonal_positions(pos: Position, board_shape: Shape): Position[][][] {
    const diagonal_positions: Position[][][] = []
    diagonal_range.forEach((ab) => {
        const a = ab[0]
        const b = ab[1]
        const highest_board_shape = board_shape[0] >= board_shape[1] ? board_shape[1] : board_shape[0]
        const dia_positions: Position[] = range(highest_board_shape).map((i) => [pos[0] + (i * a), pos[1] + (i * b)])
        const positions = split_at_position(
            filter_positions_off_board_list(
                dia_positions, board_shape
            ),
            pos
        )
    })
    return diagonal_positions
}