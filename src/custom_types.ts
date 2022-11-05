type Position = [number, number]
type Shape = [number, number]

interface Piece {
    position: Position;
    symbol: string;
    full_symbol: string;
    is_white: Colour;
    colour: Colour;
    in_play: boolean;
    has_moved: boolean;
}

enum Colour {
    White,
    Black
}

