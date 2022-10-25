cimport numpy as np

cdef class Piece:
    cdef public tuple position
    cdef public str symbol
    cdef public str full_symbol
    cdef public bint is_white
    cdef public str colour
    cdef public bint in_play
    cdef public bint has_moved

cdef class Game:
    cdef public np.ndarray board
    cdef public list moves
    cdef public bint completed
    cdef public str winner
    cdef public str turn
    cdef public str setup
    cdef public tuple shape
    cdef public str board_state