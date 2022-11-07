const KingBehaviour = require("KingBehaviour");

enum PieceCode {
    KING,
    QUEEN,
    ROOK,
    BISHOP,
    KNIGHT,
    PAWN
}


interface Piece {
	position: Position;
	symbol?: string;
	full_symbol?: PieceCode;
	is_white: boolean;
	colour?: Colour;
	in_play?: boolean;
	has_moved?: boolean;
    is_empty: boolean
}

const PIECE_CODE_OBJECT = {
    'BISHOP': PieceCode.BISHOP,
    'bishop': PieceCode.BISHOP,
    'B': PieceCode.BISHOP,
    'b': PieceCode.BISHOP,
    'ROOK': PieceCode.ROOK,
    'rook': PieceCode.ROOK,
    'R': PieceCode.ROOK,
    'r': PieceCode.ROOK,
    'KING': PieceCode.KING,
    'king': PieceCode.KING,
    'K': PieceCode.KING,
    'k': PieceCode.KING,
    'PAWN': PieceCode.PAWN,
    'pawn': PieceCode.PAWN,
    'P': PieceCode.PAWN,
    'p': PieceCode.PAWN,
    'QUEEN': PieceCode.QUEEN,
    'queen': PieceCode.QUEEN,
    'Q': PieceCode.QUEEN,
    'q': PieceCode.QUEEN,
    'KNIGHT': PieceCode.KNIGHT,
    'knight': PieceCode.KNIGHT,
    'N': PieceCode.KNIGHT,
    'n': PieceCode.KNIGHT
}
const PIECE_CODE_DICT: Map<string, PieceCode> = new Map(Object.entries(PIECE_CODE_OBJECT));

function make_piece(pos: Position, symbol: string): Piece {
    const is_white = symbol.toUpperCase() === symbol
    return {
        position: pos,
        symbol: symbol,
        full_symbol: PIECE_CODE_DICT.get(symbol),
        is_white: is_white,
        colour: is_white ? Colour.White : Colour.Black,
        in_play: true,
        has_moved: false,
    } as Piece
}

function allowed_moves(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const full_symbol = piece.full_symbol
    let allowed_moves_array: Position[] = []
    if (full_symbol === PieceCode.KING) {
        allowed_moves_array = king_allowed_moves(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.QUEEN) {
        allowed_moves_array = queen_allowed_moves(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.ROOK) {
        allowed_moves_array = rook_allowed_moves(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.BISHOP) {
        allowed_moves_array = bishop_allowed_moves(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.KNIGHT) {
        allowed_moves_array = knight_allowed_moves(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.PAWN) {
        allowed_moves_array = pawn_allowed_moves(piece, board, pos, is_white)
    }
    return allowed_moves_array
}

function get_allowed_moves(piece: Piece, board: Array2D): Position[] {
    const pos = piece.position
    let new_positions = allowed_moves(piece, board, pos, piece.is_white)
    return new_positions.filter((p) => check_position_is_on_board(p, board.shape))
}

function allowed_takes(piece: Piece, board: Array2D, pos: Position, is_white: boolean): Position[] {
    const full_symbol = piece.full_symbol
    let allowed_takes_array: Position[] = []
    if (full_symbol === PieceCode.KING) {
        allowed_takes_array = king_allowed_takes(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.QUEEN) {
        allowed_takes_array = queen_allowed_takes(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.ROOK) {
        allowed_takes_array = rook_allowed_takes(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.BISHOP) {
        allowed_takes_array = bishop_allowed_takes(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.KNIGHT) {
        allowed_takes_array = knight_allowed_takes(piece, board, pos, is_white)
    } else if (full_symbol === PieceCode.PAWN) {
        allowed_takes_array = pawn_allowed_takes(piece, board, pos, is_white)
    }
    return allowed_takes_array
}

function get_allowed_takes(piece: Piece, board: Array2D): Position[] {
    const pos = piece.position
    let new_positions = allowed_takes(piece, board, pos, piece.is_white)
    return new_positions.filter((p) => check_position_is_on_board(p, board.shape))
}

function get_legal_moves(piece: Piece, board: Array2D): Position[] {
    const allowed_moves = get_allowed_moves(piece, board)
    const allowed_takes = get_allowed_takes(piece, board)
    const allowed: Position[] = [...allowed_moves, ...allowed_takes]
    return [...new Set(allowed)]
}

