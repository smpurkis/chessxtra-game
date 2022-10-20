cdef class Piece:
    cdef public tuple position
    cdef public str symbol
    cdef public str full_symbol
    cdef public bint is_white
    cdef public str colour
    cdef public bint in_play
    cdef public bint has_moved
