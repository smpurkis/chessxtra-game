import { Array2D } from "./Array";
import { Colour, Position, Shape } from "./custom_types";
import { get_allowed_moves, get_allowed_takes, get_legal_moves, make_piece, Piece, PieceCode } from "./pieces/Piece";

interface Game {
	board: Array2D;
	moves: string[];
	completed: boolean;
	winner?: Colour;
	turn: Colour;
	setup: string;
	shape: Shape;
	board_state?: string | null;
}

export const range = (n: number) => [...Array(n).keys()]

export function initialize_game(shape: Shape = [6, 4], setup = "rnbk\npppp", board_state = ""): Game {
	if (board_state !== "") {
		shape = [board_state.split("\n").length, board_state.split("\n")[0].length]
	}
	const data = []
	for (const i of range(shape[0])) {
		const row = []
		for (const j of range(shape[1])) {
			const empty_piece: Piece = {
				is_empty: true
			} as Piece
			row.push(empty_piece)
		} 
		data.push(row)
	}
	const array2d: Array2D = {
		shape: shape,
		data: data,
	} as Array2D
	let game: Game = {
		shape: shape,
		setup: setup,
		board: array2d,
		board_state: board_state,
		completed: false,
		moves: [],
		turn: Colour.White,
	} as Game
	if (board_state === "") {
		game = start_setup(game, setup)
	} else {
		game = setup_position(game, board_state)
	}
	return game
}

function check_completed(game: Game): void {
	const white_pieces = get_pieces(game, Colour.White)
	const black_pieces = get_pieces(game, Colour.Black)
	const white_king_exists = white_pieces.filter((p) => p.full_symbol == PieceCode.KING).length === 1 
	const black_king_exists = black_pieces.filter((p) => p.full_symbol == PieceCode.KING).length === 1
	if (!game.completed) {
		if (white_king_exists && black_king_exists) {
		} else if (white_king_exists && !black_king_exists) {
			game.winner = Colour.White
			game.completed = true
		} else if (!white_king_exists && black_king_exists) {
			game.winner = Colour.Black
			game.completed = true
		}
	} else {
		throw "Should not get here"
	}
}

function setup_position(game: Game, board_state: string): Game {
	const setup_lines = board_state.split("\n")
	for (const [row_no, lines] of setup_lines.entries()) {
		for (const col_no of range(lines.length)) {
			const piece_code = lines[col_no]
			if (piece_code == "-") {
				game.board.data[row_no][col_no] = {
					is_empty: true
				} as Piece
			} else {
				game.board.data[row_no][col_no] = make_piece([row_no, col_no], piece_code)
			}
		}
	}
	return game
}

function start_setup(game: Game, setup_position: string): Game {
	const setup_lines = setup_position.split("\n")

	for (const i of range(setup_lines[0].length)) {
		const piece_code = setup_lines[0][i]
		const col_no = i
		game.board.data[0][col_no] = make_piece([0, col_no], piece_code)
		game.board.data[game.board.shape[0] - 1][col_no] = make_piece([game.board.shape[0] - 1, col_no], piece_code.toUpperCase())
	}

	for (const i of range(setup_lines[1].length)) {
		const piece_code = setup_lines[1][i]
		const col_no = i
		game.board.data[1][col_no] = make_piece([1, col_no], piece_code)
		game.board.data[game.board.shape[0] - 2][col_no] = make_piece([game.board.shape[0] - 2, col_no], piece_code.toUpperCase())
	}

	return game
}

export function get_all_legal_moves(game: Game, colour: Colour): Map<Piece, Position[]> {
	const legal_moves: Map<Piece, Position[]> = new Map()
	for (const row_no of range(game.board.shape[0])) {
		for (const col_no of range(game.board.shape[1])) {
			const piece: Piece = game.board.data[row_no][col_no]
			if (!piece.is_empty) {
				if (piece.in_play && piece.colour == colour) {
					const piece_legal_moves = get_legal_moves(piece, game.board)
					if (piece_legal_moves.length > 0) {
						legal_moves.set(piece, piece_legal_moves)
					}
				}
			}
		}
	}
	return legal_moves
}

function get_pieces(game: Game, colour: Colour | null = null): Piece[] {
	const pieces = []
	for (const row_no of range(game.board.shape[0])) {
		for (const col_no of range(game.board.shape[1])) {
			const piece: Piece = game.board.data[row_no][col_no]
			if (!piece.is_empty) {
				if (colour === null || piece.in_play && piece.colour == colour) {
					pieces.push(piece)
				}
			}
		}
	}
	return pieces
}

export function move(game: Game, pos_1: Position, pos_2: Position): boolean {
	const piece = game.board.data[pos_1[0]][pos_1[1]]

	if (piece.is_empty) {
		throw "Trying to move an empty square"
	}

	const allowed_moves = get_allowed_moves(piece, game.board)
	const allowed_takes = get_allowed_takes(piece, game.board)
	const allowed_set = new Set([...allowed_moves, ...allowed_takes])

	if (allowed_set.has(pos_2)) {
		throw `Illegal Move: position 1: ${pos_1}, position 2: ${pos_2}`
	}
	

	let move = `${piece.symbol}${pos_1[0]}${pos_2[1]}`

	if (allowed_takes.includes(pos_2)) {
		let take_piece: Piece = game.board.data[pos_2[0]][pos_2[1]]
		take_piece.in_play = false
		take_piece.position = [-1, -1]
		move = `${move}${take_piece.symbol}${pos_2[0]}${pos_2[1]}`
	} else {
		move = `${move}${pos_2[0]}${pos_2[1]}`
	}

	game.board.data[pos_1[0]][pos_1[1]] = {
		is_empty: true
	} as Piece
	game.board.data[pos_2[0]][pos_2[1]] = piece
	piece.position = pos_2

	game.moves.push(move)
	game.turn = game.turn === Colour.Black ? Colour.White : Colour.Black
	check_completed(game)

	return false
}