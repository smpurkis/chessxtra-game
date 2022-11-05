interface Game {
	board: Array2D;
	moves: string[];
	completed: boolean;
	winner: string;
	turn: string;
	setup: string;
	shape: Shape;
	board_state?: string;
}
