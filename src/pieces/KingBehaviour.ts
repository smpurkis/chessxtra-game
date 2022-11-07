function king_allowed_moves(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const surrounding_positions = get_surrounding_positions(pos, board.shape)
    let filt_all_ms: Position[] = []
    surrounding_positions.forEach((move_pos) => {
        const mp_piece = board.data[move_pos[0]][move_pos[1]]
        if (mp_piece.is_empty) {
            filt_all_ms.push(move_pos)
        }
    })
    return filt_all_ms
}

function king_allowed_takes(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const surrounding_positions = get_surrounding_positions(pos, board.shape)
    let filt_all_ts: Position[] = []
    surrounding_positions.forEach((take_pos) => {
        const tp_piece = board.data[take_pos[0]][take_pos[1]]
        if (!tp_piece.is_empty) {
            if (tp_piece.is_white != piece.is_white){
                filt_all_ts.push(take_pos)
            }
        }
    })
    return filt_all_ts
}