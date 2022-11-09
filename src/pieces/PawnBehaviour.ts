function pawn_allowed_moves(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const index = is_white ? -1 : 1
    let new_positions: Position[] = [[pos[0] + index, pos[1]]]
    new_positions = new_positions.filter((p) => check_position_is_on_board(p, board.shape))
    let filt_all_ms: Position[] = []
    for (const move_pos of new_positions) {
        const mp_piece = board.data[move_pos[0]][move_pos[1]]
        if (mp_piece.is_empty) {
            filt_all_ms.push(move_pos)
        }
    }
    return filt_all_ms
}

function pawn_allowed_takes(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const index = is_white ? -1 : 1
    let new_positions: Position[] = [-1, 1].map((row_i) => [pos[0] + index, pos[1] + row_i])
    new_positions = new_positions.filter((p) => check_position_is_on_board(p, board.shape))
    let filt_all_ts: Position[] = []
    for (const take_pos of new_positions) {
        const tp_piece = board.data[take_pos[0]][take_pos[1]]
        if (!tp_piece.is_empty) {
            if (tp_piece.is_white != piece.is_white){
                filt_all_ts.push(take_pos)
            }
        }
    }
    return filt_all_ts
}