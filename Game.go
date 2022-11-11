package main

type Game struct {
	board Array2D
	moves []string
	completed bool
	winner Colour
	turn Colour
	setup string
	shape Shape
}