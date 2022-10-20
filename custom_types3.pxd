from dataclasses import dataclass

@dataclass
cdef class Piece:
    cdef tuple position
    cdef str symbol
    cdef str full_symbol
    cdef bint is_white
    cdef str colour
    cdef bint in_play
    cdef bint has_moved
