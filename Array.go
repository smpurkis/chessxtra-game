package main

import "math"

type Array2D struct {
	data  []Piece
	shape Shape
}

func dist(pos1 Position, pos2 Position) int {
	return int(math.Abs(float64(pos1[0])-float64(pos2[0]))) -
		int(math.Abs(float64(pos1[1])-float64(pos2[1])))
}
