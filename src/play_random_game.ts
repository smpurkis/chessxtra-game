import { get_all_legal_moves, initialize_game, move, range } from "./Game";

const cliProgress = require('cli-progress');


function run_random_games(n: number): void {
    let outcomes = new Map()
    outcomes.set(Colour.White, 0)
    outcomes.set(Colour.Black, 0)
    const pbar = new cliProgress.SingleBar({}, cliProgress.Presets.shades_classic);
    pbar.start(n, 0)
    for (const _ of range(n)) {
        let game = initialize_game()
        while (!game.completed) {
            const legal_moves = get_all_legal_moves(game, game.turn)
            const legal_move_pieces = [...legal_moves.keys()]
            const chosen_piece = legal_move_pieces[Math.floor(Math.random() * legal_move_pieces.length)]
            const legal_move_positions: Position[] = legal_moves.get(chosen_piece)!
            const chosen_move = legal_move_positions[Math.floor(Math.random() * legal_move_positions.length)]
        
            move(game, chosen_piece.position, chosen_move)
        }
        outcomes.set(game.winner, outcomes.get(game.winner) + 1)
    }
    console.log(outcomes)
}

function main(): void {
    const startTime = performance.now()
    run_random_games(500)
    console.log(performance.now() - startTime)
}

main();
