use crate::pieces::*;
use crate::{array::check_position_is_on_board, game::Colour};
use phf::phf_map;
use std::{fmt::Display};

use crate::types::{Array2D, PieceClass, Position, Shape};

static PIECE_CODE_HASHMAP: phf::Map<&'static str, PieceClass> = phf_map! {
    "B" => PieceClass::Bishop,
    "BISHOP" => PieceClass::Bishop,
    "K" => PieceClass::King,
    "KING" => PieceClass::King,
    "KNIGHT" => PieceClass::Knight,
    "N" => PieceClass::Knight,
    "P" => PieceClass::Pawn,
    "PAWN" => PieceClass::Pawn,
    "Q" => PieceClass::Queen,
    "QUEEN" => PieceClass::Queen,
    "R" => PieceClass::Rook,
    "ROOK" => PieceClass::Rook,
    "b" => PieceClass::Bishop,
    "bishop" => PieceClass::Bishop,
    "k" => PieceClass::King,
    "king" => PieceClass::King,
    "knight" => PieceClass::Knight,
    "n" => PieceClass::Knight,
    "p" => PieceClass::Pawn,
    "pawn" => PieceClass::Pawn,
    "q" => PieceClass::Queen,
    "queen" => PieceClass::Queen,
    "r" => PieceClass::Rook,
    "rook" => PieceClass::Rook,
};
#[derive(Clone, Debug, Hash, PartialEq, Eq)]
pub struct Piece {
    pub(crate) position: Position,
    pub(crate) symbol: String,
    pub(crate) full_symbol: PieceClass,
    pub(crate) is_white: bool,
    pub(crate) colour: Colour,
    pub(crate) in_play: bool,
    has_moved: bool,
}

impl Piece {
    pub fn new(position: Position, symbol: String) -> Self {
        let symbol_is_upper = symbol.to_uppercase() == symbol;

        Piece {
            position,
            symbol: symbol.clone(),
            full_symbol: PIECE_CODE_HASHMAP[&symbol as &str],
            is_white: symbol_is_upper,
            colour: if symbol_is_upper {
                Colour::White
            } else {
                Colour::Black
            },
            in_play: true,
            has_moved: false,
        }
    }
}

impl Display for Piece {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "{}", self.symbol)
    }
}

fn allowed_moves(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    let full_symbol = piece.full_symbol;
    match full_symbol {
        PieceClass::King => KingBehaviour::allowed_moves(piece, board, pos, shape, is_white),
        PieceClass::Queen => QueenBehaviour::allowed_moves(piece, board, pos, shape, is_white),
        PieceClass::Rook => RookBehaviour::allowed_moves(piece, board, pos, shape, is_white),
        PieceClass::Bishop => BishopBehaviour::allowed_moves(piece, board, pos, shape, is_white),
        PieceClass::Knight => KnightBehaviour::allowed_moves(piece, board, pos, shape, is_white),
        PieceClass::Pawn => PawnBehaviour::allowed_moves(piece, board, pos, shape, is_white),
    }
}

pub(crate) fn get_allowed_moves(piece: &Piece, board: &Array2D, shape: &Shape) -> Vec<Position> {
    let new_positions = allowed_moves(piece, board, &piece.position, shape, piece.is_white);
    let new_positions = new_positions
        .into_iter()
        .filter(|pos| check_position_is_on_board(pos, shape))
        .collect();
    new_positions
}

fn allowed_takes(
    piece: &Piece,
    board: &Array2D,
    pos: &Position,
    shape: &Shape,
    is_white: bool,
) -> Vec<Position> {
    let full_symbol = piece.full_symbol;
    match full_symbol {
        PieceClass::King => KingBehaviour::allowed_takes(piece, board, pos, shape, is_white),
        PieceClass::Queen => QueenBehaviour::allowed_takes(piece, board, pos, shape, is_white),
        PieceClass::Rook => RookBehaviour::allowed_takes(piece, board, pos, shape, is_white),
        PieceClass::Bishop => BishopBehaviour::allowed_takes(piece, board, pos, shape, is_white),
        PieceClass::Knight => KnightBehaviour::allowed_takes(piece, board, pos, shape, is_white),
        PieceClass::Pawn => PawnBehaviour::allowed_takes(piece, board, pos, shape, is_white),
    }
}

pub(crate) fn get_allowed_takes(piece: &Piece, board: &Array2D, shape: &Shape) -> Vec<Position> {
    let new_positions = allowed_takes(piece, board, &piece.position, shape, piece.is_white);
    let new_positions = new_positions
        .into_iter()
        .filter(|pos| check_position_is_on_board(pos, shape))
        .collect();
    new_positions
}

pub(crate) fn get_legal_moves(piece: &Piece, board: &Array2D, shape: &Shape) -> Vec<Position> {
    let mut allowed_moves: Vec<Position> = get_allowed_moves(piece, board, shape);
    let mut allowed_takes: Vec<Position> = get_allowed_takes(piece, board, shape);
    allowed_moves.append(&mut allowed_takes);
    allowed_moves.sort_unstable();
    allowed_moves.dedup();
    allowed_moves
}
