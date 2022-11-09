
function queen_allowed_moves(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const col_row_positions = get_col_row_positions(pos, board.shape)
    const diagonal_positions = get_diagonal_positions(pos, board.shape)
    const position_lines = [col_row_positions, diagonal_positions].flat()
    let filt_all_ms: Position[] = []
    for (const positions of position_lines) {
        for (let dir_positions of positions) {
            dir_positions.sort()
            for (const move_pos of dir_positions) {
                const mp_piece = board.data[move_pos[0]][move_pos[1]]
                if (mp_piece.is_empty) {
                    filt_all_ms.push(move_pos)
                } else {
                    break
                }
            }
        }
    }
    return filt_all_ms
}

function queen_allowed_takes(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const col_row_positions = get_col_row_positions(pos, board.shape)
    const diagonal_positions = get_diagonal_positions(pos, board.shape)
    const position_lines = [col_row_positions, diagonal_positions].flat()
    let filt_all_ms: Position[] = []
    for (const positions of position_lines) {
        for (let dir_positions of positions) {
            dir_positions.sort()
            for (const move_pos of dir_positions) {
                const tp_piece = board.data[move_pos[0]][move_pos[1]]
                if (!tp_piece.is_empty) {
                    if (tp_piece.is_white !== piece.is_white) {
                        filt_all_ms.push(move_pos)
                    }
                    break
                }
            }
        }
    }
    return filt_all_ms}