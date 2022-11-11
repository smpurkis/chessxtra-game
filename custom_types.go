package main

type Position []int
type Shape []int

type Colour int

const (
	White int = 1
	Black     = 2
)

type Piece struct {
	position    Position
	symbol      string
	full_symbol string
	is_white    bool
	colour      string
	in_play     bool
	has_moved   bool
}
